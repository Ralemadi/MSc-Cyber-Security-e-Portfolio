# Collaborative Discussion 3 – Secure Coding Practices

## Activity Overview

The original authentication system contains several security weaknesses that should be addressed before it can be considered suitable for real-world use. The identified weaknesses are classified using the MITRE Common Weakness Enumeration (CWE) taxonomy, while the refactoring measures are informed by OWASP secure coding guidance (MITRE, 2026; OWASP Foundation, n.d.).

## Identified Weaknesses

### CWE-256 – Plaintext Storage of a Password

Passwords are stored directly in plaintext, so anyone who gains access to the stored data could read them. In the refactored version, passwords are salted and hashed using bcrypt, and bcrypt.checkpw() is used during authentication.

### CWE-89 – SQL Injection

The task identifies admin' OR '1'='1 as an SQL injection or logic flaw. However, the supplied Python code does not construct or execute an SQL query, so this input would not bypass authentication as written. If database functionality were introduced later, parameterised queries should be used to prevent SQL injection.

### CWE-521 – Weak Password Requirements

The original system accepts weak passwords such as admin123 and password, increasing the likelihood of password guessing. The refactored version improves the password policy by enforcing a minimum password length of 12 characters during registration.

### CWE-20 – Improper Input Validation

The original code does not validate username or password inputs. The refactored version checks input types, strips leading and trailing spaces from usernames, restricts usernames to an approved format, and applies password validation during registration.

### CWE-307 – Improper Restriction of Excessive Authentication Attempts

The original system allows unlimited login attempts. The refactored version tracks failed attempts and temporarily locks the account after five unsuccessful authentication attempts.

### Application Logic Flaw – Duplicate Username Registration

The original system does not enforce username uniqueness, allowing multiple user objects to be registered with the same username. The refactored version checks whether the username already exists and rejects duplicate registrations before creating a new user.

## Refactored Authentication Controls

The final implementation includes:

- bcrypt password hashing and salting.
- bcrypt-based password verification.
- username type and format validation.
- minimum 12-character password validation.
- duplicate-username protection.
- failed-attempt tracking.
- temporary account lockout after five failed attempts.
- reset of the failed-attempt counter after successful authentication.

## Execution Testing

The refactored authentication system was tested to verify the implemented security controls. The following tests were performed:

1. User registration: A new user was registered successfully.
2. Duplicate username registration: A second registration using the same username was rejected.
3. Correct password authentication: Authentication returned True.
4. Incorrect password authentication: Authentication returned False.
5. Account lockout: Five consecutive failed login attempts triggered the temporary lockout mechanism.
6. Authentication during lockout: The correct password was rejected while the account was locked.
7. Authentication after lockout expiry: After the 60-second lockout period expired, the correct password was accepted successfully.

## Peer Discussion

### My reply to Séba Daher

While reviewing Séba Daher’s refactored authentication code, I noticed that add_user() did not check whether a username already existed. Because self.users is a dictionary, registering the same username again would overwrite the existing password hash. I therefore raised this issue and suggested adding a duplicate-user check before storing the new hash. I also agreed with his observation that the SQL-injection example in the original task would not execute as SQL because the supplied implementation does not perform an SQL query.
![My reply to Séba Daher](images/my%20replay%20to%20S%C3%A9ba%20Daher%20.png)

### Séba Daher’s reply to my comment

Séba replied to my comment and confirmed that re-registering the same username would replace the existing password hash, causing the old password to stop working and the new one to take over. He described this as a potential account-takeover route and added a simple duplicate-user check to his code. I found this useful because it confirmed that the issue I identified was not only a code-quality concern, but also an application-logic security risk.
![Séba Daher reply to my comment](images/S%C3%A9ba%20Daher%20replay%20to%20my%20comment%20.png)

### Séba Daher’s reply to my initial post

In response to my initial post, Séba highlighted the value of mapping the identified weaknesses to CWE categories and agreed with the temporary account lockout approach. He also pointed out that my _validate_password() function checks only password length, meaning predictable passwords could still be accepted. He suggested checking for common or known breached passwords and strengthening the lockout behaviour if repeated lockouts occur. I specifically agree with his point that password length alone may still allow predictable passwords. The 12-character minimum is appropriate for this exercise, while a production system could use broader password screening and a more adaptive lockout policy.
![Séba Daher reply to my post](images/S%C3%A9ba%20Daher%20replay%20to%20my%20post.png)

## Files

- [Unit 7 Collaborative Discussion 3 PDF](PDF/Unit%207%20Collaborative%20Discussion%203.pdf)
- [Authentication_System.html](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-7/Collaborative%20Discussion/code/Authentication_System.html)
- [Unit 7 e-Portfolio Page](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-7/unit-7.html)
- [Return to Unit 7 ](../)

## Reflection

This unit changed the way I look at authentication code. Before this exercise, I mainly focused on whether authentication worked correctly. The refactoring showed that secure authentication also depends on password storage, input validation, account-registration rules and the way repeated failures are handled.

The collaborative discussion was also valuable because it demonstrated how peer review can identify weaknesses that are easy to overlook. The duplicate-username issue showed that application logic can create a security risk even without a conventional vulnerability, while the feedback on password quality showed that a secure implementation can still be strengthened further.

## References

- MITRE. (2026) *CWE – Common Weakness Enumeration*. Available at: https://cwe.mitre.org/ (Accessed: 6 September 2026).
- OWASP Foundation. (no date) *Secure Coding Practices – Quick Reference Guide*. Available at: https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/stable-en/ (Accessed: 6 September 2026).
- OWASP Foundation. (no date) *Authentication Cheat Sheet*. Available at: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html (Accessed: 5 September 2026).
- OWASP Foundation. (no date) *Password Storage Cheat Sheet*. Available at: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html (Accessed: 5 September 2026).
