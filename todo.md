## TODO

### Enities
- Context:
  - id: str
  - phone_number: str
  - created_at: str
  - messages: Message[]

- Message:
  - id: str
  - author: str
  - body: str

- ChatCompletion:
  - model: str
  - messages: str[]

- Content:
  - id: str
  - answer: str
  - summary: str
  - service_order: ServiceOrder
  - follow_up: int
  - check_status: CheckStatus

- ServiceOrder:
  - product: str
  - quantity: str

- CheckStatus:
  - id: str
  - success_message: str
  - error_message: str

### Controllers
- chat_controller

### Services
- chat_service

### Repositories
- context_repository

