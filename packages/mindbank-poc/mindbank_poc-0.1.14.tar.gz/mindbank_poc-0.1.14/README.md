# Mindbank PoC

Proof of Concept для платформы Mindbank - системы сбора и обработки данных из различных источников.

## Архитектура

Система построена по модульному принципу и включает следующие компоненты:

1. **Core** - основные компоненты системы:
   - Buffer - буферизация и агрегация входящих данных
   - Storage - хранение данных
   - Queue - асинхронная обработка агрегатов
   - Normalizer - преобразование агрегатов в нормализованные единицы
   - Knowledge Store - хранение нормализованных единиц
   - Security - управление интеграционными ключами и токенами доступа

2. **API** - REST API для приема данных:
   - Ingest API - прием сырых данных и агрегатов
   - Connector API - управление жизненным циклом коннекторов
   - Admin API - административные функции с защитой
   - Query API (планируется) - доступ к сохраненным данным

3. **Connectors** - коннекторы для различных источников данных:
   - Debug - генерация тестовых данных
   - FileSystem - чтение файлов из файловой системы
   - Telegram (планируется) - сбор данных из Telegram

### Поток данных

```
Коннекторы → Регистрация → Handshake → RawEntry → [буферизация] → Aggregate → [очередь] → 
Normalizer → [провайдеры нормализации] → NormalizedUnit → Knowledge Store
```

### Система безопасности

Система использует двухуровневый подход к безопасности:

1. **Интеграционные ключи** - долгоживущие токены для идентификации типов коннекторов
   - Управляются администратором через защищенные эндпоинты
   - Ограничены типами поддерживаемых коннекторов
   - Используются только для регистрации коннекторов

2. **Токены доступа** - короткоживущие токены для авторизации коннекторов
   - Генерируются при регистрации коннектора
   - Обновляются при изменении конфигурации
   - Используются для отправки данных и handshake

3. **Административный доступ** - базовая аутентификация для административных эндпоинтов
   - Защита эндпоинтов управления интеграционными ключами
   - Защита эндпоинтов управления коннекторами

## Модульная независимость

Все компоненты системы спроектированы как независимые модули с минимальными перекрестными зависимостями:

1. **Core** - базовые функции, используемые другими модулями
2. **API** - зависит только от Core
3. **Connectors** - полностью независимые модули, зависящие только от HTTP библиотек для взаимодействия с API

Каждый модуль имеет свой набор зависимостей, которые устанавливаются только при необходимости использования конкретного модуля, что позволяет:
- Уменьшить объем зависимостей
- Изолировать проблемы между модулями
- Развивать компоненты независимо друг от друга

## Нормализация данных

Система использует провайдерную архитектуру для нормализации данных с возможностью fallback:

1. **Transcript Provider** - преобразование аудио/видео в текст
   - **OpenAI Whisper API** - основной провайдер для транскрипции
   - **Fallback Provider** - локальный провайдер для работы в offline-режиме

2. **Caption Provider** - генерация описаний изображений
   - **OpenAI GPT-4V** - основной провайдер для описания изображений
   - **Fallback Provider** - локальный провайдер для работы в offline-режиме

3. **Embed Provider** - векторизация текста
   - **OpenAI Embedding API** - основной провайдер для векторизации
   - **Fallback Provider** - локальный провайдер для работы в offline-режиме

4. **Classifier Provider** - классификация контента
   - **OpenAI GPT** - основной провайдер для классификации
   - **Fallback Provider** - локальный провайдер для работы в offline-режиме

Нормализатор поддерживает два режима работы:
- **Online** - использование внешних API для обработки данных (OpenAI)
- **Offline** - использование локальных fallback-провайдеров

Конфигурация нормализатора управляется через переменные окружения в `.env` файле:

```env
# Настройки нормализатора
NORMALIZER_OFFLINE_MODE=false
NORMALIZER_TRANSCRIPT_PROVIDER=openai
NORMALIZER_CAPTION_PROVIDER=openai
NORMALIZER_EMBED_PROVIDER=openai
NORMALIZER_CLASSIFIER_PROVIDER=openai

# Настройки OpenAI API
OPENAI_API_KEY=your-api-key-here
OPENAI_ORGANIZATION_ID=your-org-id-here

# Модели OpenAI
OPENAI_WHISPER_MODEL=whisper-1
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
OPENAI_CAPTION_MODEL=gpt-4o-mini
OPENAI_CLASSIFIER_MODEL=gpt-4o-mini

# Флаги включения провайдеров 
NORMALIZER_ENABLE_TRANSCRIPT=true
NORMALIZER_ENABLE_CAPTION=true
NORMALIZER_ENABLE_EMBED=true
NORMALIZER_ENABLE_CLASSIFIER=true
```

## Спецификация коннекторов

Подробная спецификация для разработки коннекторов доступна в файле [CONNECTOR_SPEC.md](CONNECTOR_SPEC.md).

Основные принципы коннекторов:
- Единый интерфейс взаимодействия с Ingest API
- Независимость от ядра системы
- Собственные зависимости и конфигурация
- Единая модель данных для всех коннекторов
- Безопасный процесс регистрации и аутентификации
- Жизненный цикл с управляемыми состояниями (`stage`, `enabled`), включая поддержку сложного многошагового онбоардинга через FSM.

### Жизненный цикл коннектора

1. **Регистрация** - коннектор регистрируется в системе, используя интеграционный ключ. При регистрации он передает свою `config_schema` (схему финальной конфигурации), опционально `config` (начальную конфигурацию), и `setup_details` (если требуется сложная первоначальная настройка через собственный UI/CLI коннектора).
2. **Handshake / FSM Sync (Онбоардинг)** - 
    - **Простой онбоардинг/Конфигурация:** Если `setup_details` не предоставлены, коннектор может сразу перейти в состояние `READY` (если `config` валидна и `skip_periodic_handshake: true`, или `config` валидна и `skip_periodic_handshake: false`), либо в `CONFIGURATION` (если `config` невалидна/отсутствует, а `config_schema` требует поля). В состоянии `CONFIGURATION` администратор настраивает коннектор через Mindbank API.
    - **Сложный онбоардинг (FSM):** Если при регистрации были предоставлены `setup_details.setup_url` (и `skip_periodic_handshake: false`), коннектор переходит в состояние `SETUP_REQUIRED`. Администратор использует `setup_url` для настройки коннектора через его собственный интерфейс. После завершения настройки в своем UI, коннектор отправляет полную итоговую конфигурацию в Mindbank API (`POST /connectors/{id}/config`). Для более сложных, интерактивных сценариев онбоардинга, где требуется несколько шагов обмена данными между UI Mindbank и логикой коннектора, используется FSM-протокол: UI Mindbank вызывает эндпоинты `/onboard/...`, а коннектор синхронизируется с FSM Ingest API через эндпоинты `/fsm/...` (см. [CONNECTOR_SPEC.md](CONNECTOR_SPEC.md) для деталей).
3. **Handshake (Операционный режим)** - После онбоардинга и валидной конфигурации (коннектор в `stage: READY`), коннектор периодически выполняет `GET /connectors/{id}/handshake` для синхронизации состояния, получения обновленной конфигурации или нового токена доступа (если не используется `skip_periodic_handshake: true`).
4. **Отправка данных** - передача данных (`RawEntry`) на эндпоинт `POST /connectors/{id}/data` с использованием актуального `access_token`.
5. **Управление** - обновление конфигурации (`PATCH /connectors/{id}` администратором), включение/отключение (`POST /connectors/{id}/toggle` администратором), сброс конфигурации или полный сброс (`POST /connectors/{id}/reset-config`, `POST /connectors/{id}/reset-setup` коннектором).
6. **(Опционально) Уведомление об изменении динамических опций** - Коннектор может уведомить Ingest API (`POST /connectors/{id}/fsm/notify_dynamic_config_update`) о том, что его динамические опции конфигурации изменились, чтобы API запросил их обновление через FSM-протокол.

## Документация

### Техническое задание и ход реализации

- [HUB_INTEGRATION_TZ.md](HUB_INTEGRATION_TZ.md) - Техническое задание по интеграции Hub и доработке платформы
- [IMPLEMENTATION_LOG.md](IMPLEMENTATION_LOG.md) - Журнал реализации задач из технического задания
- [MindBank_Hub_Concept.md](MindBank_Hub_Concept.md) - Концепция Hub-интерфейса
- [MindBank-as-global-info-core.md](MindBank-as-global-info-core.md) - Концепция MindBank как глобального информационного ядра

### Спецификация коннекторов

Подробная спецификация для разработки коннекторов доступна в файле [CONNECTOR_SPEC.md](CONNECTOR_SPEC.md).

## Installation

### Простая установка

```bash
# Установка пакета со всеми основными зависимостями
pip install mindbank-poc
```

При такой установке будут автоматически установлены все основные компоненты:
- Ядро системы (core)
- OpenAI провайдеры
- Телеграм-коннектор
- API компоненты

### Выборочная установка

```bash
# Установка только с выбранными компонентами
pip install "mindbank-poc[core]"  # Только ядро системы
pip install "mindbank-poc[api]"   # API компоненты и ядро
pip install "mindbank-poc[connectors-telegram]"  # Только Telegram коннектор
pip install "mindbank-poc[connectors-filesystem]"  # Только FileSystem коннектор
pip install "mindbank-poc[connectors-debug]"  # Только Debug коннектор

# Установка всех компонентов включая тестовые
pip install "mindbank-poc[all]"
```

## Running

### API

Запуск API:

```bash
# Установка зависимостей
uv pip install -e '.[api]'

# Запуск API (вариант 1)
python -m uvicorn mindbank_poc.api.main:app --reload --port 8000

# Запуск API (вариант 2)
uv run uvicorn mindbank_poc.api.main:app --reload --port 8000

# Запуск API с помощью команды run-core (после установки пакета)
run-core --host localhost --port 8000 --reload

# Запуск API с указанием директории для хранения данных
run-core --host localhost --port 8000 --data-dir ~/.mindbank/core_data
```

Обратите внимание: команда `uv run python uvicorn mindbank_poc.api.main:app --reload --port 8000` некорректна, так как `uvicorn` - это отдельная команда, а не аргумент для python.

### Защищенные API

Запуск API с защитой административных эндпоинтов:

```bash
# Способ 1: Конфигурация через .env файл
AUTH_ADMIN_USERNAME=admin
AUTH_ADMIN_PASSWORD_HASH=bcrypt_hash_of_your_password
AUTH_ADMIN_API_KEY=your-admin-master-key

# Запуск API
uvicorn mindbank_poc.api.main:app --reload --port 8000
```

```bash
# Способ 2: Прямая передача через аргументы командной строки
run-core --host 0.0.0.0 --port 8000 --admin-key your-admin-master-key
```

Для доступа к защищенным административным API необходимо использовать один из способов аутентификации:
1. HTTP Basic Auth с указанными username и password
2. Authorization header с мастер-ключом: `Authorization: Bearer your-admin-master-key`

### Connectors

#### Debug Connector

```bash
# Установка зависимостей
uv pip install -e '.[connectors-debug]'

# Запуск Debug коннектора
python -m mindbank_poc.connectors.debug.client --batch-size 5 --total 20
```

#### FileSystem Connector

```bash
# Установка зависимостей
uv pip install -e '.[connectors-filesystem]'

# Запуск FileSystem коннектора
python -m mindbank_poc.connectors.filesystem.client ./data/input --extensions .txt,.md,.json
```

#### Telegram Connector

```bash
# Установка зависимостей
uv pip install -e '.[connectors-telegram]'

# Запуск Telegram коннектора (вариант 1)
python -m mindbank_poc.connectors.telegram.main --api-url http://localhost:8000 --integration-key your-integration-key

# Запуск Telegram коннектора с помощью команды run-tg-connector (после установки пакета)
run-tg-connector --api-url http://localhost:8000 --integration-key your-integration-key

# Запуск Telegram коннектора с указанием директории для хранения состояния
run-tg-connector --api-url http://localhost:8000 --integration-key your-integration-key --state-dir ~/.mindbank/telegram
```

### MindBank Client

Универсальный клиент для запуска компонентов системы через командную строку.

```bash
# Установка зависимостей
uv pip install -e '.[all]'

# Запуск только API-сервера (Core)
mind-client core --host 0.0.0.0 --port 8000 --reload

# Запуск только Telegram-коннектора
mind-client telegram --api-url http://localhost:8000 --integration-key your-integration-key

# Запуск и API-сервера, и Telegram-коннектора одновременно
mind-client all --host 0.0.0.0 --port 8000 --integration-key your-integration-key
```

### Standalone CLI команды

После установки пакета командой `pip install mindbank-poc` доступны следующие команды:

#### Запуск ядра системы (Core API)
```bash
# Базовый запуск ядра
run-core --host 0.0.0.0 --port 8000

# С дополнительными опциями
run-core --host 0.0.0.0 --port 8000 --offline-mode --reload

# С указанием директории для хранения данных
run-core --host 0.0.0.0 --port 8000 --data-dir ~/.mindbank/core_data

# С указанием мастер-ключа администратора для доступа к защищенным API
run-core --host 0.0.0.0 --port 8000 --admin-key your-admin-master-key
```

#### Запуск Telegram коннектора
```bash
# Базовый запуск Telegram коннектора
run-tg-connector --api-url http://localhost:8000 --integration-key your-integration-key

# С указанием директории для хранения состояния
run-tg-connector --api-url http://localhost:8000 --integration-key your-integration-key --state-dir ~/.mindbank/telegram
```

#### Запуск нормализатора
```bash
# Запуск нормализатора на существующем агрегате
mindbank-normalizer --jsonl-file data/ingest_jsonl/aggregates.jsonl

# Запуск в offline режиме (использовать fallback провайдеры)
mindbank-normalizer --jsonl-file data/ingest_jsonl/aggregates.jsonl --offline
```

### Normalizer

#### Тестирование нормализатора

```bash
# Установка зависимостей
uv pip install -e '.[cli]'

# Запуск нормализатора на существующем агрегате
mindbank-normalizer --jsonl-file data/ingest_jsonl/aggregates.jsonl

# Запуск в offline режиме (использовать fallback провайдеры)
mindbank-normalizer --jsonl-file data/ingest_jsonl/aggregates.jsonl --offline

# Принудительное использование OpenAI провайдеров
mindbank-normalizer --jsonl-file data/ingest_jsonl/aggregates.jsonl --openai

# Сохранение результата в файл
mindbank-normalizer --jsonl-file data/ingest_jsonl/aggregates.jsonl --output data/knowledge_store/test_unit.jsonl
```

#### Конфигурация нормализатора в .env

```env
# Настройки OpenAI API
OPENAI_API_KEY=your-api-key-here
OPENAI_ORGANIZATION_ID=your-org-id-here

# Модели OpenAI
OPENAI_WHISPER_MODEL=whisper-1
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
OPENAI_CAPTION_MODEL=gpt-4o-mini
OPENAI_CLASSIFIER_MODEL=gpt-4o-mini

# Настройки нормализатора
NORMALIZER_OFFLINE_MODE=false
NORMALIZER_TRANSCRIPT_PROVIDER=openai
NORMALIZER_CAPTION_PROVIDER=openai
NORMALIZER_EMBED_PROVIDER=openai
NORMALIZER_CLASSIFIER_PROVIDER=openai

# Флаги включения провайдеров 
NORMALIZER_ENABLE_TRANSCRIPT=true
NORMALIZER_ENABLE_CAPTION=true
NORMALIZER_ENABLE_EMBED=true
NORMALIZER_ENABLE_CLASSIFIER=true
```

## Development

### Installation

```bash
# Клонирование репозитория
git clone git@gitlab.involve.software:ml/mindbank-poc.git
cd mindbank-poc

# Установка всех зависимостей для разработки
uv pip install -e '.[all]'
```

### Testing

```bash
# Запуск всех тестов
pytest

# Запуск тестов для конкретного модуля
pytest tests/core
pytest tests/api
```

## Integration Keys for Connectors

MindBank uses integration keys as a secure way to authenticate connectors with the Core API. These keys are used to authorize connector instances to interact with MindBank's knowledge graph and processing pipelines.

### How Integration Keys Work

1. **Generation**: Integration keys are generated by the Core API when a connector is registered or through dedicated endpoints.
2. **Usage**: The integration key serves as an authentication token for the connector, ensuring secure communication with Core API.
3. **Revocation**: Keys can be revoked if compromised or no longer needed, and new keys can be generated.

### Integration Key Management

Integration keys can be managed in various ways:

- **Via Hub UI**: The ConnectorSettingsDialog allows viewing, generating, and revoking integration keys for installed connectors.
- **Programmatically**: The `IntegrationKeyService` provides methods to create, retrieve, and revoke integration keys.
- **API Endpoints**: Core API exposes endpoints for integration key management:
  - `/integration-keys` - For general key management (GET/POST)
  - `/integration-keys/{key_id}` - For specific key operations (GET)
  - `/integration-keys/{key_id}/revoke` - For revoking a specific key (POST)
  - `/connectors/{connector_id}/integration-key` - For connector-specific key generation (POST)
  - `/connectors/{connector_id}/revoke-key` - For revoking connector-specific keys (POST)

### Manual Connector Installation

For connectors that run outside of the Hub (such as on remote servers), you can use the manual installation method:

1. Select a connector in the Hub's "Available Connectors" section
2. Choose "Manual" as the installation method
3. The Hub will generate an integration key automatically
4. Use this key with the Core API URL in your connector's environment configuration:
   ```

## Публикация на PyPI

Для публикации пакета на PyPI выполните следующие шаги:

1. **Обновите версию пакета** в файле `pyproject.toml` (поле `version`). PyPI не примет публикацию с уже существующей версией.

2. Убедитесь, что у вас есть файл `.pypirc` в корне проекта с вашими PyPI credentials. Пример:

   ```ini
   [pypi]
   username = __token__
   password = pypi-***your-token-here***
   ```

3. Запустите скрипт сборки и публикации:

   ```bash
   ./build_and_publish.sh
   ```

   Этот скрипт:
   - удаляет старые сборки
   - устанавливает необходимые инструменты (`build`, `twine`)
   - собирает проект (`python -m build`)
   - публикует пакет на PyPI через twine, используя `.pypirc`

Если нужно опубликовать на TestPyPI, отредактируйте `.pypirc` и команду публикации в скрипте.