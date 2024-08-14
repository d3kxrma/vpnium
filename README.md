# VPNium

VPNium is a Python library for managing a VPN extension for Chrome WebDriver. It provides a convenient way to control and interact with a VPN extension within your Python scripts.

## Installation

To install VPNium, you can use pip:

```shell
pip install VPNium
```

## Usage

Here is an example of how to use VPNium in your Python script:

```python
from VPNium import VPNium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from driverium import Driverium

# Set up Chrome options
options = Options()
options.add_argument("--headless=new")

# Set up Chrome service
service = Service(Driverium().get_driver())

# Create VPNium instance
vpnium = VPNium(options, service)

# Get driver instance
driver = vpnium.driver

# Get available servers
servers = vpnium.get_available_servers()
print(servers)

# Connect to a server
vpnium.connect_to_server("United Kingdom (UK)")

# Disconnect from the server
vpnium.disconnect()

```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the [VPNium GitHub repository](https://github.com/d3kxrma/vpnium).


## License

VPNium is licensed under the MIT License. See the [LICENSE](https://github.com/d3kxrma/vpnium/blob/main/LICENSE) file for more information.
