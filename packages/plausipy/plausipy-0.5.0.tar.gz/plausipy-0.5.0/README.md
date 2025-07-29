# Plausipy - Privacy-First Usage Analytics for Python Applications

Plausipy is a powerful Python package designed to provide developers with insightful usage analytics while placing a strong emphasis on user privacy. It enables applications to gather meaningful data about their usage without compromising the trust of their users. 
Plausipy focuses on transparency, user control, and ethical data management, ensuring that developers can leverage analytics responsibly while respecting user privacy.

## What data can be tracked with Plausipy?

Plausipy allows developers to track various aspects of their applications' usage, offering valuable insights that can help improve performance, user experience, and overall functionality. The package collects data across three main categories:

1. **Runtime Information**: Understand how your application performs during execution, including:
   - RAM usage
   - Execution time
   - Exit code

2. **System Information**: Gain insights into the environments where your application runs, including:
   - Platform (e.g., Windows, macOS, Linux)
   - Python version

3. **Location Information**: Collect geographical data that can help tailor user experiences, such as:
   - Country
   - Region
   - Timezone

## Consent

Asking users for consent is crucial for maintaining trust and transparency, but it should not hinder the user experience. Striking this balance is sensitive.

Plausipy will present a single dialog box to users, requesting consent for collecting usage statistics. Users can select their options interactively using the arrow keys or by pressing the corresponding key.

To minimize user requests, Plausipy will maintain a global user consent state that applies to all packages. Additionally, users can utilize the Plausipy CLI tool to whitelist or blacklist individual packages.

## Privacy-First Approach

Plausipy is built with a commitment to user privacy at its core. Here’s how it achieves this:

### 1. No Personal Data Collection

Plausipy does not collect any personal user data, including email addresses, names, or IP addresses. This ensures that users' identities remain confidential, fostering a trustful relationship between developers and users.

### 2. Give Users Control

Plausipy empowers users to control their data by providing them with the ability to customize the information they want to share and to opt-out of any tracking.

### 3. Tracking Profiles

Plausipy employs a robust framework to manage data collection through three distinct tracking profiles, each designed to enhance privacy and control:

- **User Scope**: A unique user ID is assigned to track usage data across different packages. This allows for the creation of user profiles that aggregate usage information without ever linking to real-world identities. Importantly, this user ID is anonymized, ensuring that it cannot be traced back to an individual.

- **Package Scope**: Within this scope, usage data from multiple executions of the same package can be linked to the same user ID. However, data from different packages is kept separate, preventing any cross-contamination of information. This means that while developers can gain insights into how a specific package is used, they cannot connect this data to a user’s activity across different packages.

- **Anonymous Scope**: Each execution of the application is treated independently under this scope. A unique ID is assigned to each execution, ensuring that no profiling or user behavior tracking can occur based on the ID. The unique ID is stored locally as a reference and can be used to request the deletion of tracking records for a specific run.

### 4. User Transparency

Users have the right to know what data is being collected about them. With Plausipy, users can view all collected data through the Plausipy CLI tool. This transparency empowers users to understand and manage their data, reinforcing trust between developers and users.

## Future Enhancements

Plausipy is continuously evolving. Future updates will include features that allow users to request the deletion of tracking records for specific packages or individual runs, further enhancing user control over their data. We also plan to support custom properties to give more flexibility to developers in tracking additional data points.  

## Getting Started

To integrate Plausipy into your project, follow these steps:

```bash
# add dependency 
uv add plausipy

# install via pip
pip install plausipy
```

Once installed, login to [plausipy.com](plausipy.com) and create a package to obtain a Package Key.

![Copy package key from plausipy.com portal.](images/portal_get_package_key.png)

To start collecting usage statistics, initialize Plausipy at the top of your application's entrypoint script.

```python
import plausipy
plausipy.app(key="sayrrCCNbXY70ci6xHn8qlYwKyAUawgp", delay_consent=True)

# all other imports
# import x 

# ask for consent
plausipy.consent()
```

If you are developing a library, use the `plausipy.lib` method instead. 
This will automatically register your package for collection of usage information until requested by the main application.

```python
import plausipy
plausipy.lib(key="sayrrCCNbXY70ci6xHn8qlYwKyAUawgp")
```
