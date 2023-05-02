# App structure:

Directory Tree:

```
├── repositories
├── resources
├── services
├── ui
└── user_data
```

Descriptions:

- **repositories**: Modules that are responsible for abstracting away database read/write operations from other
  application
  logic by implementing the _repository_ pattern.
- **resources**: Contains resources like icons and font, but also the application database `.sql` script for creating
  the application database.
- **services**: This directory will to contain modules for classes that create the application logic by using
  lower-level
  components, like in the **repositories** directory.
- **ui**: Contains modules for specific "views" in the app, like login view and main view. **ui** also contains
  modules that handle switching between those views.
- user_data: This is a directory where the app writes it data when a user uses it. It will contain the application
  database once it's created.
