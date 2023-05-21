# Bima Insurance Platform

Blockchain based weather index insurance platform.

![](./docs/img/cover.png)

## Tech Stack 

- `Flask`
- `Algorand`
- `Postgres`


## Setup

To run create a `.env` file in the root directory and populate with the following

``` 
SECRET_FLASK=
TESTNET_ALGOD_API_KEY=
TESTNET_ALGOD_ADDRESS=https://testnet-algorand.api.purestake.io/ps2
TESTNET_ALGOINDEXER_SERVER=https://testnet-algorand.api.purestake.io/idx2
ACCOUNT1_ADDRESS=
ACCOUNT1_MNEMONIC=
ACCOUNT2_ADDRESS=
ACCOUNT2_MNEMONIC=
ADMIN_USERNAME=
ADMIN_PASSWORD=
DATABASE_URL=
ADMIN_SWATCH=readable
LOG_WITH_GUNICORN=True
CONFIG_CLASS =config.DevelopmentConfig
```

## App Description

The detailed app description is [here](/docs/README.md)

## License

    Copyright 2023 Tatenda Muvhu

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
