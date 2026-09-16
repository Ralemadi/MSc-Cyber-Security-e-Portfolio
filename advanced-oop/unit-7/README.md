# Unit 7 – Secure Coding Practices in Object-Oriented Programming

**Programme:** MSc Cyber Security  
**Module:** Advanced Object-Oriented Design and Programming  
**Unit:** 7 – Secure Coding Practices in Object-Oriented Programming

## Unit Overview

This unit developed my understanding of security as part of software design rather than something added after development is complete. I learned that weaknesses in object-oriented applications can arise from both technical vulnerabilities and insecure implementation choices, and that secure coding requires careful control of how data is accepted, processed and used within an application.

The practical work applied these ideas to a user authentication system. The original implementation contained weaknesses related to plaintext password storage, weak password requirements, missing input validation and unrestricted authentication attempts. Through the refactoring and collaborative discussion, I also examined duplicate username registration as an application-logic security risk and critically assessed the SQL-injection example provided in the task.

## Learning Outcomes

After completing this unit, I was able to:

- Explain why secure coding should be considered during software design and implementation.
- Identify security weaknesses and insecure implementation choices in existing application code.
- Apply secure coding techniques including input validation, password hashing and authentication controls.
- Refactor vulnerable code while preserving its intended functionality.
- Analyse authentication logic for application-level security risks, such as duplicate username registration and unrestricted login attempts.
- Use MITRE CWE and OWASP guidance to support identified weaknesses and appropriate mitigations.

## Main Artefact

The main artefact for this unit was Collaborative Discussion 3, which focused on reviewing and refactoring a vulnerable user authentication system. I identified weaknesses in the supplied implementation and mapped them to relevant CWE categories to support the analysis. The refactored version uses bcrypt for password hashing, validates usernames and passwords, rejects duplicate usernames and temporarily locks accounts after repeated failed authentication attempts.

The exercise also encouraged critical evaluation of the supplied SQL-injection example. Because the original Python code does not construct or execute an SQL query, the input admin' OR '1'='1 would not bypass authentication as written. This demonstrated the importance of analysing how a vulnerability actually applies to the code rather than assuming that a malicious-looking input automatically represents a successful attack. If database functionality were introduced later, parameterised queries should be used to reduce SQL-injection risk.

The identified weaknesses were mapped to the following categories:

- **CWE-256 – Plaintext Storage of a Password**
- **CWE-89 – SQL Injection**
- **CWE-521 – Weak Password Requirements**
- **CWE-20 – Improper Input Validation**
- **CWE-307 – Improper Restriction of Excessive Authentication Attempts**
- **Application Logic Flaw – Duplicate Username Registration**

## Artefacts and Evidence

| Artefact | Description |
|---|---|
| [Collaborative Discussion 3 PDF](Collaborative%20Discussion/PDF/Unit%207%20Collaborative%20Discussion%203.pdf) | Full discussion submission, refactored code and execution evidence |
| [Authentication System](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-7/Collaborative%20Discussion/code/Authentication_System.html) | Refactored authentication source code |
| [Collaborative Discussion ](Collaborative%20Discussion/) | Summary of the discussion, implementation and peer feedback |
| [Unit 7 e-Portfolio Page](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-7/unit-7.html) | Unit summary, artefacts, reflection and peer feedback |

## Collaborative Discussion – Peer Feedback

### My reply to Séba Daher

While reviewing Séba Daher’s refactored authentication code, I noticed that add_user() did not check whether a username already existed. Because self.users is a dictionary, registering the same username again would overwrite the existing password hash. I therefore raised this issue and suggested adding a duplicate-user check before storing the new hash. I also agreed with his observation that the SQL-injection example in the original task would not execute as SQL because the supplied implementation does not perform an SQL query.
![My reply to Séba Daher](images/my%20replay%20to%20S%C3%A9ba%20Daher%20.png)

### Séba Daher’s reply to my comment

Séba replied to my comment and confirmed that re-registering the same username would replace the existing password hash, causing the old password to stop working and the new one to take over. He described this as a potential account-takeover route and added a simple duplicate-user check to his code. I found this useful because it confirmed that the issue I identified was not only a code-quality concern, but also an application-logic security risk.
![Séba Daher reply to my comment](images/S%C3%A9ba%20Daher%20replay%20to%20my%20comment%20.png)

### Séba Daher’s reply to my initial post

In response to my initial post, Séba highlighted the value of mapping the identified weaknesses to CWE categories and agreed with the temporary account lockout approach. He also pointed out that my _validate_password() function checks only password length, meaning predictable passwords could still be accepted. He suggested checking for common or known breached passwords and strengthening the lockout behaviour if repeated lockouts occur. I specifically agree with his point that password length alone may still allow predictable passwords. The 12-character minimum is appropriate for this exercise, while a production system could use broader password screening and a more adaptive lockout policy.
![Séba Daher reply to my post](images/S%C3%A9ba%20Daher%20replay%20to%20my%20post.png)

## Reflection

This unit changed the way I look at authentication code. Before this exercise, I mainly focused on whether authentication worked correctly. The refactoring showed that secure authentication also depends on password storage, input validation, account-registration rules and the way repeated failures are handled.

The collaborative discussion was also valuable because it demonstrated how peer review can identify weaknesses that are easy to overlook. The duplicate-username issue showed that application logic can create a security risk even without a conventional vulnerability, while the feedback on password quality showed that a secure implementation can still be strengthened further.

The work in this unit improved my ability to connect code-level findings with recognised weakness classifications and practical mitigations. It also strengthened my approach to reviewing authentication logic from both a technical and application logic perspective.

In future security related development, I intend to apply secure coding principles from the design stage, validate user input, protect stored credentials, control repeated authentication attempts and consider application-logic abuse cases during code review.

## References

- MITRE (2026) *CWE – Common Weakness Enumeration*. Available at: https://cwe.mitre.org/ (Accessed: 6 September 2026).
- OWASP Foundation (n.d.) *Secure Coding Practices – Quick Reference Guide*. Available at: https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/stable-en/ (Accessed: 6 September 2026).
- OWASP Foundation (n.d.) *Authentication Cheat Sheet*. Available at: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html (Accessed: 5 September 2026).
- OWASP Foundation (n.d.) *Password Storage Cheat Sheet*. Available at: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html (Accessed: 5 September 2026).
