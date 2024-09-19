## TODO

### Enities
- message:
  - id: str
  - body: str

- chat_completion:
  - model: str
  - messages: str[]

- content:
  - id: str
  - answer: str
  - context: str
  - service_order:
    - product: str
    - quantity: str
  - followup: int
  - check_status:
    - id: str 
    - successMessage: str 
    - errorMessage: str


### Controllers
- chat_controller

### Services
- chat_service

### Repositories
- context_repository

