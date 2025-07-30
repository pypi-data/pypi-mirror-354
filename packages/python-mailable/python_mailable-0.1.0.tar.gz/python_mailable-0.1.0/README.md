# Python Mailable

**Python Mailable** is an email builder for Python, inspired by Laravel's Mailable class. It provides a clean and reusable structure for defining, composing, and sending emails with rich context and templates.

> [!IMPORTANT]  
> We currently only support _rendering_ emails, not sending them.
>
> This package helps you build and render email content using templates, but you need to handle email sending yourself with your own SMTP client or email delivery service.
>
> Use the `.render()` method to get your email body, and then integrate with any mail-sending solution you prefer.

## Features

- Define email classes with subjects, recipients, and templates
- Pass context to templates for dynamic rendering
- Attach files easily
- Designed for clarity, testability, and reusability

## Usage

### Creating a Mailable

To define a custom email, subclass `Mailable` and implement the `build()` method. Use the fluent API to configure the mail.

```python
from dataclasses import dataclass
from mailable import Mailable

@dataclass
class OrderShipped(Mailable):
    user: User  # Your domain model or DTO

    def build(self):
        return (
            self.to(self.user.email)
                .subject("Your order has shipped!")
                .template("emails/order_shipped.html")
                .with_context({"user": self.user})
        )

```

### Sending the email

```python
user = User(email="jane.doe@example.com", name="Jane Doe")

email = OrderShipped(user).build()
email.send()  # Sends using the built-in SMTP backend
```

> 💡 **Want to use your own mail client instead?**  
> You can call `email.render()` to get the subject, body, and recipient info — and pass that into your own delivery system.
