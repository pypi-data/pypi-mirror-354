'''
WechatTools
---------------
该模块中封装了一系列关于PC微信的工具,主要包括:检测微信运行状态;\n
打开微信主界面内绝大多数界面\n
模块:\n
---------------
Tools:一些关于PC微信的工具,以及13个open方法用于打开微信主界面内所有能打开的界面\n
API:打开指定公众号与微信小程序以及视频号,可为微信内部小程序公众号自动化操作提供便利\n
------------------------------------
函数:\n
函数为上述模块内的所有方法\n
--------------------------------------
使用该模块的方法时,你可以:\n
```
from pywechat.WechatTools import API
API.open_wechat_miniprogram(name='问卷星')
```
或者:\n
```
from pywechat import WechatTools as wt
wt.open_wechat_miniprogram(name='问卷星')
```
或者:\n
```
from pywechat.WechatTools import open_wechat_miniprogram
open_wechat_miniprogram(name='问卷星')
```
或者:\n
```
from pywechat import open_wechat_miniprogram
open_wechat_miniprogram(name='问卷星')
```
'''
############################依赖环境###########################
import os
import re
import time
import winreg
import win32api
import pyautogui
import win32gui
import win32con
import subprocess
import win32com.client
from pywinauto import mouse,Desktop
from pywinauto.controls.uia_controls import ListItemWrapper
from pywinauto.controls.uia_controls import ListViewWrapper
from .Errors import NetWorkNotConnectError
from .Errors import NoSuchFriendError
from .Errors import ScanCodeToLogInError
from .Errors import NoResultsError,NotFriendError,NotInstalledError
from .Errors import NoChatHistoryError
from .Errors import NoSuchMessageError
from .Errors import ElementNotFoundError
from .Errors import WrongParameterError
from pywinauto.findwindows import ElementNotFoundError
from pywinauto import WindowSpecification
from pywechat4.Uielements import Login_window,Main_window,SideBar,Independent_window,Buttons,Texts,Menus,TabItems
from pywechat4.WinSettings import Systemsettings 
##########################################################################################
Login_window=Login_window()
Main_window=Main_window()
SideBar=SideBar()
Independent_window=Independent_window()
Buttons=Buttons()
Texts=Texts()
Menus=Menus()
TabItems=TabItems()
pyautogui.FAILSAFE = False#防止鼠标在屏幕边缘处造成的误触

class Tools():
    '''该模块中封装了关于PC微信的工具\n
    以及13个open方法用于打开微信主界面内所有能打开的界面\n
    ''' 
    @staticmethod
    def is_wechat_running():
        '''
        该方法通过检测当前windows系统的进程中\n
        是否有WeChat.exe该项进程来判断微信是否在运行
        '''
        wmi=win32com.client.GetObject('winmgmts:')
        processes=wmi.InstancesOf('Win32_Process')
        for process in processes:
            if process.Name.lower() == 'Weixin.exe'.lower():
                return True
        return False
            
    @staticmethod
    def find_wechat_path(copy_to_clipboard:bool=True):
        '''该方法用来查找微信的路径,无论微信是否运行都可以查找到\n
            copy_to_clipboard:\t是否将微信路径复制到剪贴板\n
        '''
        if Tools.is_wechat_running():
            wmi=win32com.client.GetObject('winmgmts:')
            processes=wmi.InstancesOf('Win32_Process')
            for process in processes:
                if process.Name.lower() == 'Weixin.exe'.lower():
                    exe_path=process.ExecutablePath
                    if exe_path:
                        # 规范化路径并检查文件是否存在
                        exe_path=os.path.abspath(exe_path)
                        wechat_path=exe_path
            if copy_to_clipboard:
                Systemsettings.copy_text_to_windowsclipboard(wechat_path)
                print("已将微信程序路径复制到剪贴板")
            return wechat_path
        else:
            #windows环境变量中查找WeChat.exe路径
            wechat_environ_path=[path for path in dict(os.environ).values() if 'Weixin.exe' in path]#
            if wechat_environ_path:
                if copy_to_clipboard:
                    Systemsettings.copy_text_to_windowsclipboard(wechat_path)
                    print("已将微信程序路径复制到剪贴板")
                return wechat_environ_path
            if not wechat_environ_path:
                try:
                    reg_path=r"Software\Tencent\Weixin"
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path) as key:
                        Installdir=winreg.QueryValueEx(key,"InstallPath")[0]
                    wechat_path=os.path.join(Installdir,'Weixin.exe')
                    if copy_to_clipboard:
                        Systemsettings.copy_text_to_windowsclipboard(wechat_path)
                        print("已将微信程序路径复制到剪贴板")
                    return wechat_path
                except FileNotFoundError:
                    raise NotInstalledError
        
    @staticmethod
    def is_VerticalScrollable(List:ListViewWrapper):
        '''
        该方法用来判断微信内的列表是否可以垂直滚动\n
        说明:\t微信内的List均为UIA框架,无句柄,停靠在右侧的scrollbar组件无Ui\n
        且列表还只渲染可见部分,因此需要使用UIA的iface_scorll来判断\n
        Args:
            List:微信内control_type为List的列表
        '''
        try:
            #如果能获取到这个属性,说明可以滚动
            List.iface_scroll.CurrentVerticallyScrollable
            return True
        except Exception:#否则会引发NoPatternInterfaceError,此时返回False
            return False
        
    
    @staticmethod
    def set_wechat_as_environ_path():
        '''该方法用来自动打开系统环境变量设置界面,将微信路径自动添加至其中\n'''
        os.environ.update({"__COMPAT_LAYER":"RUnAsInvoker"})
        subprocess.Popen(["SystemPropertiesAdvanced.exe"])
        time.sleep(2)
        systemwindow=win32gui.FindWindow(None,u'系统属性')
        if win32gui.IsWindow(systemwindow):#将系统变量窗口置于桌面最前端
            win32gui.ShowWindow(systemwindow,win32con.SW_SHOW)
            win32gui.SetWindowPos(systemwindow,win32con.HWND_TOPMOST,0,0,0,0,win32con.SWP_NOMOVE|win32con.SWP_NOSIZE)    
        pyautogui.hotkey('alt','n',interval=0.5)#添加管理员权限后使用一系列快捷键来填写微信刻路径为环境变量
        pyautogui.hotkey('alt','n',interval=0.5)
        pyautogui.press('shift')
        pyautogui.typewrite('wechatpath')
        try:
            Tools.find_wechat_path()
            pyautogui.hotkey('Tab',interval=0.5)
            pyautogui.hotkey('ctrl','v')
            pyautogui.press('enter')
            pyautogui.press('enter')
            pyautogui.press('esc')
        except Exception:
            pyautogui.press('esc')
            pyautogui.hotkey('alt','f4')
            pyautogui.hotkey('alt','f4')
            raise NotInstalledError
 
    @staticmethod
    def judge_wechat_state():
        '''该方法用来判断微信运行状态'''
        time.sleep(1.5)
        if Tools.is_wechat_running():
            window=win32gui.FindWindow(Main_window.MainWindow['class_name'],Main_window.MainWindow['title'])
            if win32gui.IsIconic(window):
                return '主界面最小化'
            elif win32gui.IsWindowVisible(window):
                return '主界面可见'
            else:
                return '主界面不可见'
        else:
            return "微信未打开"
        
    @staticmethod
    def judge_independant_window_state(window:dict):
        '''该方法用来判断微信内独立于微信主界面的窗口的状态\n'''
        time.sleep(1)
        handle=win32gui.FindWindow(window.get('class_name'),None)
        if win32gui.IsIconic(handle):
            win32gui.SetForegroundWindow(handle)
            return '界面最小化'
        elif win32gui.IsWindowVisible(handle):  
            return '界面可见'
        else:
            return '界面未打开,需进入微信打开'
       
        
    @staticmethod
    def move_window_to_center(Window:dict=Main_window.MainWindow,Window_handle:int=0):
        '''该方法用来将已打开的界面移动到屏幕中央并返回该窗口的windowspecification实例,使用时需注意传入参数为窗口的字典形式\n
        需要包括class_name与title两个键值对,任意一个没有值可以使用None代替\n
        Args:
            Window:\tpywinauto定位元素kwargs参数字典
            Window_handle:\t窗口句柄\n
        '''
        desktop=Desktop(**Independent_window.Desktop)
        class_name=Window['class_name']
        title=Window['title'] if 'title' in Window else None
        if Window_handle==0:
            handle=win32gui.FindWindow(class_name,title)
        else:
            handle=Window_handle
        screen_width,screen_height=win32api.GetSystemMetrics(win32con.SM_CXSCREEN),win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        window=desktop.window(handle=handle)
        window_width,window_height=window.rectangle().width(),window.rectangle().height()
        new_left=(screen_width-window_width)//2
        new_top=(screen_height-window_height)//2
        if screen_width!=window_width:
            win32gui.MoveWindow(handle, new_left, new_top, window_width, window_height, True)
        return window
    
    @staticmethod 
    def open_wechat(is_maximize:bool=True,wechat_path:str=None):
        def handle_login_window(login_window:WindowSpecification,is_maximize:bool):
            retry_interval=0.5
            max_retry_times=30
            counter=0
            try:
                login_button=login_window.child_window(**Login_window.LoginButton)
                login_button.set_focus()
                login_button.click_input()
                main_window=Desktop(backend='uia').window(**Main_window.MainWindow)
                while not main_window.exists():
                    counter+=1
                    time.sleep(retry_interval)
                    if counter>=max_retry_times:
                        raise NetWorkNotConnectError
                move_window_to_center(main_window=main_window,is_maximize=is_maximize)
                NetWorkErrotText=main_window.child_window(**Texts.NetWorkError)
                if NetWorkErrotText.exists():
                    main_window.close()
                    raise NetWorkNotConnectError(f'未连接网络,请连接网络后再进行后续自动化操作！')
                return main_window 
            except ElementNotFoundError:
                raise ScanCodeToLogInError
            
        def move_window_to_center(main_window:WindowSpecification,is_maximize:bool):
            handle=main_window.handle
            #以下的操作均使用win32gui实现,包括将主界面的大小,移动到前台，移动到屏幕中央
            ###################################
            #win32gui.SetWindowPos来实现移动窗口到前台来,相当于win32gui.SetForeGroundWindow()
            #但是win32gui.SetForeGroundWindow()函数可能会因为权限不足等一系列问题报错
            #所以使用win32gui.SetWindowPos()来实现类似的功能
            win32gui.SetWindowPos(handle,win32con.HWND_TOPMOST, 
            0, 0, 0, 0,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            ###########################################
            #移动窗口到屏幕中央
            screen_width,screen_height=win32api.GetSystemMetrics(win32con.SM_CXSCREEN),win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
            window_width,window_height=main_window.rectangle().width(),main_window.rectangle().height()
            new_left=(screen_width-window_width)//2
            new_top=(screen_height-window_height)//2
            if screen_width!=window_width:
                win32gui.MoveWindow(handle, new_left, new_top, window_width, window_height, True)
            ##############################
            if is_maximize:
                win32gui.ShowWindow(handle, win32con.SW_MAXIMIZE)
            if not is_maximize:
                win32gui.ShowWindow(handle,win32con.SW_SHOWDEFAULT)

        weixin_path=Tools.find_wechat_path(copy_to_clipboard=False)
        if not weixin_path:
            weixin_path=wechat_path
        # os.startfile(weixin_path)
        # time.sleep(2)
        login_window=Desktop(backend='uia').window(**Login_window.LoginWindow)
        main_window=Desktop(backend='uia').window(**Main_window.MainWindow)
        if login_window.exists():
            handle_login_window(login_window=login_window,is_maximize=is_maximize)
        if main_window.exists():
            move_window_to_center(main_window=main_window,is_maximize=is_maximize)
        return main_window
                                
    @staticmethod
    def open_settings(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来打开微信设置界面。\n
        Args:
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:微信界面是否全屏,默认全屏。\n
            close_wechat:任务结束后是否关闭微信,默认关闭\n
        '''   
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        setting=main_window.child_window(**SideBar.SettingsAndOthers)
        setting.click_input()
        settings_button=main_window.child_window(**Buttons.SettingsButton)
        settings_button.click_input()
        if close_wechat:
            main_window.close() 
        time.sleep(1)
        desktop=Desktop(**Independent_window.Desktop)
        settings_window=desktop.window(**Independent_window.SettingWindow)
        return settings_window
    
    @staticmethod                    
    def open_dialog_window(friend:str,wechat_path:str=None,search_pages:int=0,is_maximize:bool=True): 
        '''
        该方法用于打开某个好友的聊天窗口\n
        Args:
            friend:\t好友或群聊备注名称,需提供完整名称\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                  尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                  传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            search_pages:在会话列表中查询查找好友时滚动列表的次数,默认为5,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        Returns:
            (EditArea,main_window) 主界面右侧下方消息编辑区域,main_window:微信主界面
        '''
        def is_in_searh_result(friend,search_result):#查看搜索列表里有没有名为friend的listitem
            listitem=search_result.children(control_type="ListItem")
            names=[item.window_text() for item in listitem]
            if friend in names:
                return True
            else:
                return False
        #这部分代码先判断微信主界面是否可见,如果可见不需要重新打开,这在多个close_wechat为False需要进行来连续操作的方式使用时要用到
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        chat_button=main_window.child_window(**SideBar.Chats)
        #先看看当前聊天界面是不是好友的聊天界面
        current_chat=main_window.child_window(**Main_window.CurrentChatWindow)
        #如果当前主界面是某个好友的聊天界面且聊天界面顶部的名称为好友名称，直接返回结果
        if current_chat.exists() and current_chat.legacy_properties().get('Name')==friend:
                chat=current_chat
                chat.click_input()
                return chat,main_window
        else:#否则直接从顶部搜索栏出搜索结果
            chat_button=main_window.child_window(**SideBar.Chats)         
            chat_button.click_input()
            search=main_window.descendants(**Main_window.Search)[0]
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(friend)
            pyautogui.hotkey('ctrl','v')
            search_results=main_window.child_window(**Main_window.SearchResult)
            time.sleep(1)
            if is_in_searh_result(friend=friend,search_result=search_results):
                result=search_results.children(control_type='ListItem',title=friend)[0]
                result.click_input()
                chat=main_window.descendants(title=friend,control_type='Edit')[0]
                return chat,main_window #同时返回该好友的聊天窗口与主界面！若只需要其中一个需要使用元祖索引获取。
            else:
                chat_button.click_input()
                main_window.close()
                raise NoSuchFriendError

         
    @staticmethod
    def open_collections(wechat_path:str=None,is_maximize:bool=True):
        '''
        该方法用于打开收藏界面\n
        Args:
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
        '''
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        
        collections_button=main_window.child_window(**SideBar.Collections)
        collections_button.click_input()
        return main_window
    

    @staticmethod
    def open_wechat_moments(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用于打开微信朋友圈\n
        Args:
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        moments_button=main_window.child_window(**SideBar.Moments)
        moments_button.click_input()
        moments_window=Tools.move_window_to_center(Independent_window.MomentsWindow)
        moments_window.child_window(**Buttons.RefreshButton).click_input()
        if close_wechat:
            main_window.close()
        return moments_window
    
    @staticmethod
    def open_chat_files(wechat_path:str=None,wechat_maximize:bool=True,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用于打开聊天文件\n
        Args:
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            wechat_maximize:微信界面是否全屏,默认全屏\n
            is_maximize:\t聊天文件界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=wechat_maximize)

        moments_button=main_window.child_window(**SideBar.ChatFiles)
        moments_button.click_input()
        desktop=Desktop(**Independent_window.Desktop)
        filelist_window=desktop.window(**Independent_window.ChatFilesWindow)
        if is_maximize:
            filelist_window.maximize()
        if close_wechat:
            main_window.close()
        return filelist_window
    
    
    @staticmethod
    def open_contacts(wechat_path:str=None,is_maximize:bool=True):
        '''
        该方法用于打开微信通信录界面\n
        Args:
            friend:\t好友或群聊备注名称,需提供完整名称\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
        '''
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        contacts=main_window.child_window(**SideBar.Contacts)
        contacts.set_focus()
        contacts.click_input()
        cancel_button=main_window.child_window(**Buttons.CancelButton)
        if cancel_button.exists():
            cancel_button.click_input()
        ContactsLists=main_window.child_window(**Main_window.ContactsList)
        rec=ContactsLists.rectangle()
        mouse.click(coords=(rec.right-5,rec.top))
        pyautogui.press('Home')
        pyautogui.press('pageup')
        return main_window

    @staticmethod
    def open_chat_history(friend:str,TabItem:str=None,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用于打开好友聊天记录界面\n
        Args:
            friend:\t好友备注名称,需提供完整名称\n
            TabItem:\t点击聊天记录顶部的Tab选项,默认为None,可选值为:文件,图片与视频,链接,音乐与音频,小程序,视频号,日期\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为5,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        tabItems={'文件':TabItems.FileTabItem,'图片与视频':TabItems.PhotoAndVideoTabItem,'链接':TabItems.LinkTabItem,'音乐与音频':TabItems.MusicTabItem,'小程序':TabItems.MiniProgramTabItem,'Channel':TabItems.ChannelTabItem,'日期':TabItems.DateTabItem}
        if TabItem:
            if TabItem not in tabItems.keys():
                raise WrongParameterError('TabItem参数错误!')
        main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)[1]
        chat_toolbar=main_window.child_window(**Main_window.ChatToolBar)
        chat_history_button=chat_toolbar.child_window(**Buttons.ChatHistoryButton)
        chat_history_button.click_input()
        chat_history_window=Tools.move_window_to_center(Independent_window.ChatHistoryWindow)
        if TabItem:
            chat_history_window.child_window(**tabItems[TabItem]).click_input()
        if close_wechat:
            main_window.close()
        return chat_history_window,main_window

    @staticmethod
    def open_program_pane(wechat_path:str=None,is_maximize:bool=True,wechat_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来打开小程序面板\n
        Args:
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t小程序面板界面是否全屏,默认全屏。\n
            wechat_maximize:\t微信主界面是否全屏,默认全屏\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=wechat_maximize)
        program_button=main_window.child_window(**SideBar.Miniprogram_pane)
        program_button.click_input()
        if close_wechat:
            main_window.close()
        program_window=Tools.move_window_to_center(Independent_window.MiniProgramWindow)
        if is_maximize:
            program_window.maximize()
        return program_window
    
    @staticmethod
    def open_top_stories(wechat_path:str=None,is_maximize:bool=True,wechat_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用于打开看一看\n
        Args:
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t看一看界面是否全屏,默认全屏。\n
            wechat_maximize:\t微信主界面是否全屏,默认全屏\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=wechat_maximize)
        
        top_stories_button=main_window.child_window(**SideBar.Topstories)
        top_stories_button.click_input()
        desktop=Desktop(**Independent_window.Desktop)
        top_stories_window=desktop.window(**Independent_window.TopStoriesWindow)
        if is_maximize:
            top_stories_window.maximize()
        if close_wechat:
            main_window.close()
        return top_stories_window

    @staticmethod
    def open_search(wechat_path:str=None,is_maximize:bool=True,wechat_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用于打开搜一搜\n
        Args:
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t搜一搜界面是否全屏,默认全屏。\n
            wechat_maximize:\t微信主界面是否全屏,默认全屏\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=wechat_maximize)
        
        search_button=main_window.child_window(**SideBar.Search)
        search_button.click_input()
        desktop=Desktop(**Independent_window.Desktop)
        search_window=desktop.window(**Independent_window.SearchWindow)
        if is_maximize:
            search_window.maximize()
        if close_wechat:
            main_window.close()
        return search_window    

    @staticmethod
    def open_channels(wechat_path:str=None,is_maximize:bool=True,wechat_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用于打开视频号\n
        Args: 
            wechat_path:\\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t视频号界面是否全屏,默认全屏。\n
            wechat_maximize:\t微信主界面是否全屏,默认全屏\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n  
        '''
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=wechat_maximize)
        channel_button=main_window.child_window(**SideBar.Channel)
        channel_button.click_input()
        desktop=Desktop(**Independent_window.Desktop)
        channel_window=desktop.window(**Independent_window.ChannelWindow)
        if is_maximize:
            channel_window.maximize()
        if close_wechat:
            main_window.close()
        return channel_window
    
    @staticmethod
    def pull_messages(friend:str,number:int,parse:bool=True,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''该方法用来从主界面右侧的聊天区域内获取指定条数的聊天记录消息\n
        Args:
            friend:\t好友或群聊备注\n
            number:\t聊天记录条数\n
            parse:\t是否解析聊天记录为文本(主界面右侧聊天区域内的聊天记录形式为ListItem),设置为False时返回的类型为ListItem\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏法搜索好友信息打开聊天界面\n
            wechat_path:\\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信主界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        Returns:
            senders:\t发送消息的对象\n
            chatMessages:\t发送的消息\n
            list[ListItem]:\t聊天消息的ListItem形式
        '''
        senders=[]
        chatMessages=[]
        type='好友'#默认是好友
        main_window=Tools.open_dialog_window(friend=friend,search_pages=search_pages,wechat_path=wechat_path,is_maximize=is_maximize)[1]
        chat_history_button=main_window.child_window(**Buttons.ChatHistoryButton)
        if not chat_history_button.exists():#没有聊天记录按钮是公众号或其他类型的东西
            raise NotFriendError(f'{friend}不是好友，无法获取聊天记录！')
        chatList=main_window.child_window(**Main_window.FriendChatList)
        viewMoreMesssageButton=main_window.child_window(**Buttons.CheckMoreMessagesButton)
        if len(chatList.children(control_type='ListItem'))==0:
            raise NoChatHistoryError(f'你与 {friend} 没有聊天记录,无法获取聊天记录')
        video_call_button=main_window.child_window(**Buttons.VideoCallButton)
        if not video_call_button.exists():##没有视频聊天按钮是群聊
            type='群聊'
        #if message.descendants(conrol_type)是用来筛选这个消息(control_type为ListItem)内有没有按钮(消息是人发的必然会有头像按钮这个UI,系统消息比如'8:55'没有这个UI)
        chat_Messages=[message for message in chatList.children(control_type='ListItem') if message.children()[0].children(control_type='Button')]
        chat_Messages=[message for message in chat_Messages if message.window_text()!=Buttons.CheckMoreMessagesButton['title']]#查看更多消息内部也含按钮得排除掉
        #点击聊天区域侧边栏和头像之间的位置来激活滑块,不直接main_window.click_input()是为了防止点到消息
        x,y=chatList.rectangle().left+8,(main_window.rectangle().top+main_window.rectangle().bottom)//2#
        if len(chat_Messages)>=number:#聊天区域内部不需要遍历就可以获取到的消息数量大于number条
            chat_Messages=chat_Messages[-number:]#返回从后向前数number条消息
        else:#否则向上遍历
            ##########################################################
            mouse.click(coords=(chatList.rectangle().right-10,chatList.rectangle().bottom-5))
            while len(chat_Messages)<number:
                chatList.iface_scroll.SetScrollPercent(verticalPercent=0.0,horizontalPercent=1.0)
                mouse.scroll(coords=(x,y),wheel_dist=1000)
                chat_Messages=[message for message in chatList.children(control_type='ListItem') if message.children()[0].children(control_type='Button')]
                chat_Messages=[message for message in chat_Messages if message.window_text()!=Buttons.CheckMoreMessagesButton['title']]
                if not viewMoreMesssageButton.exists():#向上遍历时如果查看更多消息按钮不在存在说明已经到达最顶部,没有必要继续向上,直接退出循环
                    break
            chat_Messages=chat_Messages[-number:] 
        #######################################################
        if close_wechat:
            main_window.close()
        if parse:
            for ListItem in chat_Messages:
                sender,message=Tools.parse_message_content(ListItem,type)
                senders.append(sender)
                chatMessages.append(message)
            return senders,chatMessages
        else:
            return chat_Messages
    

   
class API():
    '''这个模块包括打开指定名称小程序,打开制定名称微信公众号的功能\n
    若有其他自动化开发者需要在微信内的这两个功能下进行自动化操作可调用此模块\n
    '''
    @staticmethod
    def open_wechat_miniprogram(name:str,load_delay:float=2.5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_program_pane:bool=True):
        '''
        该方法用于打开指定小程序\n
        Args:
            name:\t微信小程序名字\n
            load_delay:\t搜索小程序名称后等待时长,默认为2.5秒\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        desktop=Desktop(**Independent_window.Desktop)
        if Tools.judge_independant_window_state(Independent_window.MiniProgramWindow)!='界面未打开,需进入微信打开':
            HWND=win32gui.FindWindow(Independent_window.MiniProgramWindow.get('class_name'),Independent_window.MiniProgramWindow.get('title'))
            win32gui.ShowWindow(HWND,1)
            win32gui.SetForegroundWindow(HWND)
            program_window=Tools.move_window_to_center(Independent_window.MiniProgramWindow)
            miniprogram_tab=program_window.child_window(title='小程序',control_type='TabItem')
            if miniprogram_tab.exists():
                miniprogram_tab.click_input()
            else:
                program_window.close()
                program_window=Tools.open_program_pane(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        else:
            program_window=Tools.open_program_pane(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        miniprogram_tab=program_window.child_window(title='小程序',control_type='TabItem')
        miniprogram_tab.click_input()
        time.sleep(load_delay)
        try:
            more=program_window.child_window(title='更多',control_type='Text',found_index=0)#小程序面板内的更多文本
        except ElementNotFoundError:
            program_window.close()
            print('网络不良,请尝试增加load_delay时长,或更换网络')
        rec=more.rectangle()
        mouse.click(coords=(rec.right+20,rec.top-50))
        up=5
        search=program_window.child_window(control_type='Edit',title='搜索小程序')
        while not search.exists():
            mouse.click(coords=(rec.right+20,rec.top-50-up))
            search=program_window.child_window(control_type='Edit',title='搜索小程序')
            up+=5
        search.click_input()
        Systemsettings.copy_text_to_windowsclipboard(name)
        pyautogui.hotkey('ctrl','v',_pause=False)
        pyautogui.press("enter")
        time.sleep(load_delay)
        try:
            search_result=program_window.child_window(control_type="Document",class_name="Chrome_RenderWidgetHostHWND")
            text=search_result.child_window(title=name,control_type='Text',found_index=0)
            text.click_input()
            if close_program_pane:
                program_window.close()
            program=desktop.window(control_type='Pane',title=name)
            return program
        except ElementNotFoundError:
            program_window.close()
            raise NoResultsError('查无此小程序!')
        
    @staticmethod
    def open_wechat_official_account(name:str,load_delay:float=1,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用于打开指定的微信公众号\n
        Args:
            name:\t微信公众号名称\n
            load_delay:\t加载搜索公众号结果的时间,单位:s\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
        '''
        desktop=Desktop(**Independent_window.Desktop)
        try:
            search_window=Tools.open_search(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
            time.sleep(load_delay)
        except ElementNotFoundError:
            search_window.close()
            print('网络不良,请尝试增加load_delay时长,或更换网络')
        try:
            official_acount_button=search_window.child_window(**Buttons.OfficialAcountButton)
            official_acount_button.click_input()
        except ElementNotFoundError:
            search_window.close()
            print('网络不良,请尝试增加load_delay时长,或更换网络')
        search=search_window.child_window(control_type='Edit',found_index=0)
        search.click_input()
        Systemsettings.copy_text_to_windowsclipboard(name)
        pyautogui.hotkey('ctrl','v')
        pyautogui.press('enter')
        time.sleep(load_delay)
        try:
            search_result=search_window.child_window(control_type="Button",found_index=1,framework_id="Chrome")
            search_result.click_input()
            official_acount_window=desktop.window(**Independent_window.OfficialAccountWindow)
            search_window.close()
            return official_acount_window
        except ElementNotFoundError:
            search_window.close()
            raise NoResultsError('查无此公众号!')
        
    @staticmethod
    def search_channels(search_content:str,load_delay:float=1,wechat_path:str=None,wechat_maximize:bool=True,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用于打开视频号并搜索指定内容\n
        Args:
            search_content:在视频号内待搜索内容\n
            load_delay:加载查询结果的时间,单位:s\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:微信界面是否全屏,默认全屏。\n
        '''
        Systemsettings.copy_text_to_windowsclipboard(search_content)
        channel_widow=Tools.open_channels(wechat_maximize=wechat_maximize,is_maximize=is_maximize,wechat_path=wechat_path,close_wechat=close_wechat)
        search_bar=channel_widow.child_window(control_type='Edit',title='搜索',framework_id='Chrome')
        while not search_bar.exists():
            time.sleep(0.1)
            search_bar=channel_widow.child_window(control_type='Edit',title='搜索',framework_id='Chrome')
        search_bar.click_input()
        pyautogui.hotkey('ctrl','v')
        pyautogui.press('enter')
        time.sleep(load_delay)
        try:
            search_result=channel_widow.child_window(control_type='Document',title=f'{search_content}_搜索')
            return channel_widow
        except ElementNotFoundError:
            channel_widow.close()
            print('网络不良,请尝试增加load_delay时长,或更换网络')
    
    
def is_wechat_running():
    '''
    该方法通过检测当前windows系统的进程中\n
    是否有WeChat.exe该项进程来判断微信是否在运行
    '''
    wmi=win32com.client.GetObject('winmgmts:')
    processes=wmi.InstancesOf('Win32_Process')
    for process in processes:
        if process.Name.lower()=='Weixin.exe'.lower():
            return True
    return False
    

      


def open_settings(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来打开微信设置界面。注意,有时微信的设置界面会出现点击设置按钮后无法正常弹出,这是微信自身的Bug\n
    Args:
        wechat_path:微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
    ''' 
    SettingsWindowhandle=win32gui.FindWindow(Independent_window.SettingWindow.get('class_name'),Independent_window.SettingWindow.get('title'))
    if SettingsWindowhandle:
        win32gui.ShowWindow(SettingsWindowhandle,1)  
    else:
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        setting=main_window.child_window(**SideBar.SettingsAndOthers)
        setting.click_input()
        settings_menu=main_window.child_window(**Main_window.SettingsMenu)
        settings_button=settings_menu.child_window(**Buttons.SettingsButton)
        settings_button.click_input() 
        time.sleep(2)
    desktop=Desktop(**Independent_window.Desktop)
    settings_window=desktop.window(**Independent_window.SettingWindow)
    if close_wechat:
        main_window.close()
    return settings_window

def open_wechat_moments(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用于打开微信朋友圈\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    
    moments_button=main_window.child_window(**SideBar.Moments)
    moments_button.click_input()
    moments_window=Tools.move_window_to_center(Independent_window.MomentsWindow)
    moments_window.child_window(**Buttons.RefreshButton).click_input()
    if close_wechat:
        main_window.close()
    return moments_window
   
def open_wechat_miniprogram(name:str,load_delay:float=2.5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_program_pane:bool=True):
    '''
    该函数用于打开指定小程序\n
    Args:
        name:\t微信小程序名字\n
        load_delay:\t搜索小程序名称后等待时长,默认为2.5秒\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    desktop=Desktop(**Independent_window.Desktop)
    if Tools.judge_independant_window_state(Independent_window.MiniProgramWindow)!='界面未打开,需进入微信打开':
        HWND=win32gui.FindWindow(Independent_window.MiniProgramWindow.get('class_name'),Independent_window.MiniProgramWindow.get('title'))
        win32gui.ShowWindow(HWND,1)
        program_window=Tools.move_window_to_center(Independent_window.MiniProgramWindow)
        miniprogram_tab=program_window.child_window(title='小程序',control_type='TabItem')
        if miniprogram_tab.exists():
            miniprogram_tab.click_input()
        else:
            program_window.close()
            program_window=Tools.open_program_pane(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    else:
        program_window=Tools.open_program_pane(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    miniprogram_tab=program_window.child_window(title='小程序',control_type='TabItem')
    miniprogram_tab.click_input()
    time.sleep(load_delay)
    try:
        more=program_window.child_window(title='更多',control_type='Text',found_index=0)#小程序面板内的更多文本
    except ElementNotFoundError:
        program_window.close()
        print('网络不良,请尝试增加load_delay时长,或更换网络')
    rec=more.rectangle()
    mouse.click(coords=(rec.right+20,rec.top-50))
    up=5
    search=program_window.child_window(control_type='Edit',title='搜索小程序')
    while not search.exists():
        mouse.click(coords=(rec.right+20,rec.top-50-up))
        search=program_window.child_window(control_type='Edit',title='搜索小程序')
        up+=5
    search.click_input()
    Systemsettings.copy_text_to_windowsclipboard(name)
    pyautogui.hotkey('ctrl','v',_pause=False)
    pyautogui.press("enter")
    time.sleep(load_delay)
    try:
        search_result=program_window.child_window(control_type="Document",class_name="Chrome_RenderWidgetHostHWND")
        text=search_result.child_window(title=name,control_type='Text',found_index=0)
        text.click_input()
        if close_program_pane:
            program_window.close()
        program=desktop.window(control_type='Pane',title=name)
        return program
    except ElementNotFoundError:
        program_window.close()
        raise NoResultsError('查无此小程序!')
    
def open_wechat_official_account(name:str,load_delay:float=1,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用于打开指定的微信公众号\n
    Args:
        name:\t微信公众号名称\n
        load_delay:\t加载搜索公众号结果的时间,单位:s\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
    '''
    desktop=Desktop(**Independent_window.Desktop)
    try:
        search_window=Tools.open_search(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        
        time.sleep(load_delay)
    except ElementNotFoundError:
        search_window.close()
        print('网络不良,请尝试增加load_delay时长,或更换网络')
    try:
        official_acount_button=search_window.child_window(**Buttons.OfficialAcountButton)
        official_acount_button.click_input()
    except ElementNotFoundError:
        search_window.close()
        print('网络不良,请尝试增加load_delay时长,或更换网络')
    search=search_window.child_window(control_type='Edit',found_index=0)
    search.click_input()
    Systemsettings.copy_text_to_windowsclipboard(name)
    pyautogui.hotkey('ctrl','v')
    pyautogui.press('enter')
    time.sleep(load_delay)
    try:
        search_result=search_window.child_window(control_type="Button",found_index=1,framework_id="Chrome")
        search_result.click_input()
        official_acount_window=desktop.window(**Independent_window.OfficialAccountWindow)
        search_window.close()
        return official_acount_window
    except ElementNotFoundError:
        search_window.close()
        raise NoResultsError('查无此公众号!')
    
def open_contacts(wechat_path:str=None,is_maximize:bool=True):
    '''
    该函数用于打开微信通信录界面\n
    Args:
        friend:\t好友或群聊备注名称,需提供完整名称\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
    '''
    main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    contacts=main_window.child_window(**SideBar.Contacts)
    contacts.set_focus()
    contacts.click_input()
    cancel_button=main_window.child_window(**Buttons.CancelButton)
    if cancel_button.exists():
        cancel_button.click_input()
    ContactsLists=main_window.child_window(**Main_window.ContactsList)
    rec=ContactsLists.rectangle()
    mouse.click(coords=(rec.right-5,rec.top))
    pyautogui.press('Home')
    pyautogui.press('pageup')
    return main_window


def open_collections(wechat_path:str=None,is_maximize:bool=True):
    '''
    该函数用于打开收藏界面\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
    '''
    main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    collections_button=main_window.child_window(**SideBar.Collections)
    collections_button.click_input()
    return main_window

    
def open_chat_files(wechat_path:str=None,wechat_maximize:bool=True,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用于打开聊天文件\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        wechat_maximize:微信界面是否全屏,默认全屏\n
        is_maximize:\t聊天文件界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=wechat_maximize)
    moments_button=main_window.child_window(**SideBar.ChatFiles)
    moments_button.click_input()
    desktop=Desktop(**Independent_window.Desktop)
    filelist_window=desktop.window(**Independent_window.ChatFilesWindow)
    if is_maximize:
        filelist_window.maximize()
    if close_wechat:
        main_window.close()
    return filelist_window
    

def open_program_pane(wechat_path:str=None,is_maximize:bool=True,wechat_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来打开小程序面板\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t小程序面板界面是否全屏,默认全屏。\n
        wechat_maximize:\t微信主界面是否全屏,默认全屏\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=wechat_maximize)
    program_button=main_window.child_window(**SideBar.Miniprogram_pane)
    program_button.click_input()
    if close_wechat:  
        main_window.close()
    program_window=Tools.move_window_to_center(Independent_window.MiniProgramWindow)
    if is_maximize:
        program_window.maximize()
    return program_window

def open_top_stories(wechat_path:str=None,is_maximize:bool=True,wechat_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用于打开看一看\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t看一看界面是否全屏,默认全屏。\n
        wechat_maximize:\t微信主界面是否全屏,默认全屏\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=wechat_maximize)
    top_stories_button=main_window.child_window(**SideBar.Topstories)
    top_stories_button.click_input()
    desktop=Desktop(**Independent_window.Desktop)
    top_stories_window=desktop.window(**Independent_window.TopStoriesWindow)
    if is_maximize:
        top_stories_window.maximize()
    if close_wechat:
        main_window.close()
    return top_stories_window

def open_search(wechat_path:str=None,is_maximize:bool=True,wechat_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用于打开搜一搜\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t搜一搜界面是否全屏,默认全屏。\n
        wechat_maximize:\t微信主界面是否全屏,默认全屏\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=wechat_maximize)
    search_button=main_window.child_window(**SideBar.Search)
    search_button.click_input()
    desktop=Desktop(**Independent_window.Desktop)
    search_window=desktop.window(**Independent_window.SearchWindow)
    if is_maximize:
        search_window.maximize()
    if close_wechat:
        main_window.close()
    return search_window     

def open_channels(wechat_path:str=None,is_maximize:bool=True,wechat_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用于打开视频号\n
    Args: 
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t视频号界面是否全屏,默认全屏。\n
        wechat_maximize:\t微信主界面是否全屏,默认全屏\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n  
    '''
    main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=wechat_maximize)
    channel_button=main_window.child_window(**SideBar.Channel)
    channel_button.click_input()
    desktop=Desktop(**Independent_window.Desktop)
    channel_window=desktop.window(**Independent_window.ChannelWindow)
    if is_maximize:
        channel_window.maximize()
    if close_wechat:
        main_window.close()
    return channel_window



def set_wechat_as_environ_path():
    '''该函数用来自动打开系统环境变量设置界面,将微信路径自动添加至其中'''
    os.environ.update({"__COMPAT_LAYER":"RUnAsInvoker"})#添加管理员权限
    subprocess.Popen(["SystemPropertiesAdvanced.exe"])
    time.sleep(2)
    systemwindow=win32gui.FindWindow(None,u'系统属性')
    if win32gui.IsWindow(systemwindow):#将系统变量窗口置于桌面最前端
        win32gui.ShowWindow(systemwindow,win32con.SW_SHOW)
        win32gui.SetWindowPos(systemwindow,win32con.HWND_TOPMOST,0,0,0,0,win32con.SWP_NOMOVE|win32con.SWP_NOSIZE)     
    pyautogui.hotkey('alt','n',interval=0.5)#添加管理员权限后使用一系列快捷键来填写微信刻路径为环境变量
    pyautogui.hotkey('alt','n',interval=0.5)
    pyautogui.press('shift')   
    pyautogui.typewrite('wechatpath')
    try:
        Tools.find_wechat_path()
        pyautogui.hotkey('Tab',interval=0.5)
        pyautogui.hotkey('ctrl','v')
        pyautogui.press('enter')
        pyautogui.press('enter')
        pyautogui.press('esc')
    except Exception:
        pyautogui.press('esc')
        pyautogui.hotkey('alt','f4')
        pyautogui.hotkey('alt','f4')
        raise NotInstalledError
   
     
def judge_wechat_state():
    '''该函数用来判断微信运行状态'''
    time.sleep(1.5)
    if Tools.is_wechat_running():
        window=win32gui.FindWindow(Main_window.MainWindow['class_name'],Main_window.MainWindow['title'])
        if win32gui.IsIconic(window):
            return '主界面最小化'
        elif win32gui.IsWindowVisible(window):
            return '主界面可见'
        else:
            return '主界面不可见'
    else:
        return "微信未打开"
 
def move_window_to_center(Window:dict=Main_window.MainWindow,Window_handle:int=0):
    '''该函数用来将已打开的界面移动到屏幕中央并返回该窗口的windowspecification实例,使用时需注意传入参数为窗口的字典形式\n
    需要包括class_name与title两个键值对,任意一个没有值可以使用None代替\n
    Args:
        Window:\tpywinauto定位元素kwargs参数字典
        Window_handle:\t窗口句柄\n
    '''
    desktop=Desktop(**Independent_window.Desktop)
    class_name=Window['class_name']
    title=Window['title'] if 'title' in Window else None
    if Window_handle==0:
        handle=win32gui.FindWindow(class_name,title)
    else:
        handle=Window_handle
    
    screen_width,screen_height=win32api.GetSystemMetrics(win32con.SM_CXSCREEN),win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    window=desktop.window(handle=handle)
    window_width,window_height=window.rectangle().width(),window.rectangle().height()
    new_left=(screen_width-window_width)//2
    new_top=(screen_height-window_height)//2
    if screen_width!=window_width:
        win32gui.MoveWindow(handle, new_left, new_top, window_width, window_height, True)
    return window
        

def open_chat_history(friend:str,TabItem:str=None,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用于打开好友聊天记录界面\n
    Args:
        friend:\t好友备注名称,需提供完整名称\n
        TabItem:\t点击聊天记录顶部的Tab选项,默认为None,可选值为:文件,图片与视频,链接,音乐与音频,小程序,视频号,日期\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为5,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    tabItems={'文件':TabItems.FileTabItem,'图片与视频':TabItems.PhotoAndVideoTabItem,'链接':TabItems.LinkTabItem,'音乐与音频':TabItems.MusicTabItem,'小程序':TabItems.MiniProgramTabItem,'Channel':TabItems.ChannelTabItem,'日期':TabItems.DateTabItem}
    if TabItem:
        if TabItem not in tabItems.keys():
            raise WrongParameterError('TabItem参数错误!')
    main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)[1]
    chat_toolbar=main_window.child_window(**Main_window.ChatToolBar)
    chat_history_button=chat_toolbar.child_window(**Buttons.ChatHistoryButton)
    chat_history_button.click_input()
    chat_history_window=Tools.move_window_to_center(Independent_window.ChatHistoryWindow)
    if TabItem:
        chat_history_window.child_window(**tabItems[TabItem]).click_input()
    if close_wechat:
        main_window.close()
    return chat_history_window,main_window

def search_channels(search_content:str,load_delay:float=1,wechat_path:str=None,wechat_maximize:bool=True,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该方法用于打开视频号并搜索指定内容\n
    Args:
        search_content:在视频号内待搜索内容\n
        load_delay:加载查询结果的时间,单位:s\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:微信界面是否全屏,默认全屏。\n
    '''
    Systemsettings.copy_text_to_windowsclipboard(search_content)
    channel_widow=Tools.open_channels(wechat_maximize=wechat_maximize,is_maximize=is_maximize,wechat_path=wechat_path,close_wechat=close_wechat)
    search_bar=channel_widow.child_window(control_type='Edit',title='搜索',framework_id='Chrome')
    while not search_bar.exists():
        time.sleep(0.1)
        search_bar=channel_widow.child_window(control_type='Edit',title='搜索',framework_id='Chrome')
    search_bar.click_input()
    pyautogui.hotkey('ctrl','v')
    pyautogui.press('enter')
    time.sleep(load_delay)
    try:
        search_result=channel_widow.child_window(control_type='Document',title=f'{search_content}_搜索')
        return channel_widow
    except ElementNotFoundError:
        channel_widow.close()
        print('网络不良,请尝试增加load_delay时长,或更换网络')

def open_contacts_settings(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该方法用于打开通讯录设置界面\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    
    main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    
    desktop=Desktop(**Independent_window.Desktop)
    contacts=main_window.child_window(**SideBar.Contacts)
    contacts.set_focus()
    contacts.click_input()
    cancel_button=main_window.child_window(**Buttons.CancelButton)
    if cancel_button.exists():
        cancel_button.click_input()
    ContactsLists=main_window.child_window(**Main_window.ContactsList)
    #############################
    rec=ContactsLists.rectangle()
    mouse.click(coords=(rec.right-5,rec.top))
    pyautogui.press('Home')
    pyautogui.press('pageup')
    contacts_settings=main_window.child_window(**Buttons.ContactsManageButton)#通讯录管理窗口按钮 
    contacts_settings.set_focus()
    contacts_settings.click_input()
    contacts_settings_window=desktop.window(**Independent_window.ContactManagerWindow)
    if close_wechat:
        main_window.close()
    return contacts_settings_window,main_window


def match_duration(duration:str):
    '''
    该函数用来将字符串类型的时间段转换为秒\n
    Args:
        duration:持续时间,格式为:'30s','1min','1h'
    '''
    if "s" in duration:
        try:
            duration=duration.replace('s','')
            duration=float(duration)
            return duration
        except Exception:
            return None
    elif 'min' in duration:
        try:
            duration=duration.replace('min','')
            duration=float(duration)*60
            return duration
        except Exception:
            return None
    elif 'h' in duration:
        try:
            duration=duration.replace('h','')
            duration=float(duration)*60*60
            return duration
        except Exception:
            return None
    else:
        return None

def is_VerticalScrollable(List:ListViewWrapper):
    '''
    该函数用来判断微信内的列表是否可以垂直滚动\n
    说明:微信内的List均为UIA框架,无句柄,停靠在右侧的scrollbar组件无Ui\n
    且列表还只渲染可见部分,因此需要使用UIA的iface_scorll来判断\n
    Args:
        List:\t微信内control_type为List的列表
    '''
    try:
        #如果能获取到这个属性,说明可以滚动
        List.iface_scroll.CurrentVerticallyScrollable
        return True
    except Exception:#否则会引发NoPatternInterfaceError,返回False
        return False
    
