import time
import os

import requests
from chrome_version import get_chrome_version
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class VPNium():
    """
    VPNium is a class for managing a VPN extension for Chrome WebDriver.
    Args:
        options (Options): Options object for configuring the Chrome driver.
        service (Service): Service object for starting the Chrome driver.
        sleeptime (int, optional): Sleep time in seconds. Defaults to 5.
        extension_path (str, optional): Path to the VPN extension file. Defaults to None.
    """
    def __init__(self, options: Options, service: Service, sleeptime: int = 5, extension_path = None):
        self.options = options
        self.service = service
        self.sleeptime = sleeptime
        self.extension_id = "eppiocemhmnlbhjplcgkofciiegomcon"
        self.extension_url = f"chrome-extension://{self.extension_id}/popup/index.html"
        self.extension_download_url = f"https://clients2.google.com/service/update2/crx?response=redirect&prodversion={get_chrome_version()}&acceptformat=crx2,crx3&x=id%3D{self.extension_id}%26uc"
        
        if extension_path is None:
            self.extension_path = os.path.join(os.getcwd(), "vpn.crx")
        else:
            self.extension_path = extension_path
            
        self.__get_extesion()
        self.__init_driver()
        self.__init_vpn()
    
    def __get_extesion(self) -> None:
        if not os.path.isfile(self.extension_path):
            r = requests.get(self.extension_download_url)
            with open(self.extension_path, "wb") as f:
                f.write(r.content)
    
    def __init_driver(self) -> None:
        self.options.add_extension(self.extension_path)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        # self.driver.set_window_position(-1000, 500)
        # self.driver.maximize_window()
    
    def __init_vpn(self) -> None:
        self.driver.get(self.extension_url)
        time.sleep(self.sleeptime)
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        try:
            WebDriverWait(self.driver, self.sleeptime).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div/div[2]/button[2]')))
            button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div/div[2]/button[2]')
            button.click()
            time.sleep(1)
        except TimeoutException:
            pass
        
        try:
            WebDriverWait(self.driver, self.sleeptime).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div[2]/button[2]')))
            button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div[2]/button[2]')
            button.click()
            time.sleep(1)
        except TimeoutException:
            pass

    def open_extension(self, open_tab: bool = True) -> None:
        """
        Opens the extension URL in a new tab or the current tab.
        Parameters:
            open_tab (bool): Whether to open the extension URL in a new tab or the current tab. 
                             Defaults to True, which opens the URL in a new tab.
        Returns:
            None
        """
        
        if self.extension_url in self.driver.current_url:
            return
        else:
            if open_tab:
                self.driver.switch_to.new_window('tab')
                time.sleep(1)
            self.driver.get(self.extension_url)
            time.sleep(self.sleeptime)
        
        cross_btn = self.driver.find_elements(By.XPATH, '//div[@class="cross-icon simple-layout__close"]')
        if cross_btn:
            cross_btn[0].click()
            time.sleep(self.sleeptime)
    
    def close_extension(self) -> None:
        """
        Closes the extension window.
        If there are multiple window handles, it iterates through each tab and closes the tab
        that matches the extension URL. After closing the tab, it switches back to the first tab.
        If there is only one window handle, it opens a new tab, switches to it, closes the tab,
        and then switches back to the first tab.
        This method introduces delays using time.sleep() to ensure proper switching and closing of tabs.
        Returns:
            None
        """
        if len(self.driver.window_handles) > 1:
            
            for tab in self.driver.window_handles:
                self.driver.switch_to.window(tab)
                if self.extension_url in self.driver.current_url:
                    self.driver.close()
                    time.sleep(1)
                    
            self.driver.switch_to.window(self.driver.window_handles[0])
        else:
            self.driver.switch_to.new_window('tab')
            time.sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(1)
            self.driver.close()
            time.sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(1)
    
    def get_available_servers(self, close_extension: bool = True, open_tab: bool = True) -> list[str]:
        """
        Retrieves a list of available servers.
        Args:
            close_extension (bool, optional): Whether to close the extension after retrieving the servers. Defaults to True.
            open_tab (bool, optional): Whether to open a new tab before retrieving the servers. Defaults to True.
        Returns:
            list[str]: A list of available servers.
        """
        
        self.open_extension(open_tab)
        servers = []
        WebDriverWait(self.driver, self.sleeptime).until(EC.presence_of_element_located((By.CLASS_NAME, 'select-location__input')))
        input = self.driver.find_element(By.CLASS_NAME, 'select-location__input')
        input.click()
        time.sleep(self.sleeptime)
        
        ul = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/ul[2]')
        lis = ul.find_elements(By.TAG_NAME, 'li')
        
        i = 0
        while i < len(lis)//8 + 1:
            if i >= len(lis)//8:
                to_scroll = lis[-1]
                end = len(lis)
            else:
                to_scroll = lis[i*8]
                end = i*8
                
            ActionChains(self.driver).move_to_element(to_scroll).perform()
            for lli in ul.find_elements(By.TAG_NAME, 'li')[end-8:end]:
                if lli.text:
                    servers.append(lli.text.strip())
            i += 1
        if close_extension:
            self.close_extension()
        return servers
    
    def connect_to_server(self, server_name: str, timeout: int = 15, close_extension: bool = True, open_tab: bool = True) -> bool:
        """
        Connects to the specified server.
        Args:
            server_name (str): The name of the server to connect to.
            timeout (int, optional): The maximum time to wait for the connection to be established. Defaults to 15.
            close_extension (bool, optional): Whether to close the extension after connecting. Defaults to True.
            open_tab (bool, optional): Whether to open a new tab before connecting. Defaults to True.
        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        self.open_extension(open_tab)
        inputs = self.driver.find_element(By.CLASS_NAME, 'select-location__input')
        inputs.click()
        time.sleep(1)
        inputs.send_keys(server_name)
        time.sleep(1)
        ul = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/ul[2]')
        lis = ul.find_elements(By.TAG_NAME, 'li')
        connection_status = False
        if len(lis) != 0:
            lis[0].click()
            try:
                WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/span')))
                text = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/span').get_attribute('innerText')
                if "connected" in text.lower():
                    connection_status = True
            except TimeoutException:
                connection_status = False
        if close_extension:
            self.close_extension()
        return connection_status

    def disconnect(self, close_extension: bool = True, open_tab: bool = True) -> bool:
        """
        Disconnects from the VPN server.
        Args:
            close_extension (bool, optional): Whether to close the VPN extension. Defaults to True.
            open_tab (bool, optional): Whether to open a new tab. Defaults to True.
        Returns:
            bool: True if successfully disconnected, False otherwise.
        """
        self.open_extension(open_tab)
        stop_button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div/div[2]/div[4]/div/div')
        connection_status = False
        try:
            stop_button.click()
            time.sleep(1)
            text = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div/div[2]/div[4]/span').get_attribute('innerText')
            s = sum([int(x) for x in text if x.isdigit()])
            if s != 0:
                connection_status = False
            else:
                connection_status = True
        except TimeoutException:
            connection_status = False
            
        if close_extension:
            self.close_extension()
        return connection_status
        
    
    def test_servers(self, url: str, locator: tuple[str, str], timeout:int = None, servers: list = None, close_extension: bool = True, open_tab: bool = True) -> dict[str, float]:
        """
        Test the servers by connecting to each server, loading the specified URL, and measuring the time it takes to load the element specified by the locator.
        Args:
            url (str): The URL to load and test.
            locator (tuple[str, str]): A tuple containing the locator strategy and value to identify the element to wait for.
            timeout (int, optional): The maximum time to wait for the element to be present. If not provided, the default sleeptime value will be used.
            servers (list, optional): A list of servers to test. If not provided, all available servers will be tested.
            close_extension (bool, optional): Whether to close the extension after testing each server. Defaults to True.
            open_tab (bool, optional): Whether to open a new tab before testing each server. Defaults to True.
        Returns:
            dict[str, float]: A dictionary containing the server names as keys and the time taken to load the element as values. If the element is not found within the specified timeout, the value will be None.
        """
        if servers is None:
            servers = self.get_avaible_servers(close_extension=False, open_tab=False)
        
        if timeout is None:
            timeout = self.sleeptime
        
        results = {}
        
        for n, server in enumerate(servers):
            print(f"Testing server {n+1}/{len(servers)}: {server}")
            self.connect_to_server(server, False, True)
            
            self.driver.switch_to.new_window('tab')
            time.sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[1])
            try:
                start = time.perf_counter()
                self.driver.get(url)
                WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
                results[server] = time.perf_counter() - start
            except TimeoutException:
                results[server] = None
                
            self.driver.close()
            time.sleep(1)        
            self.driver.switch_to.window(self.driver.window_handles[0])
            
        return results

        