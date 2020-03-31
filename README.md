# UlisseLabBOT



## Usage:

First run the sh scripts as Root

`# sh generateVPN.sh`

Second run the Telegram Bot as User

`$ python3 main.py`



# Configuration

The configuration is stored in **config.ini file in the same directory of the main.py, the file must be named config.ini** with the following (mandatory) attributes:

```python
config.ini
```

```python
[DEFAULT]
Token = Some_Telegram_bot_Token
Chat_Id = Chat_Id_Of_The_Group_where_you_can_take_users
Vpn_Dir = Where_you_store_vpn_files
Socket_Addr = Path_to_The_Unix_Socket
Vpn_Checker = Path_to_Folder_to_Syncro_Client_Server
public_keys_file = Path_to_Yaml_File_where_Store_User_Public_Key
```

