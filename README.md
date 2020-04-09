# Demisto-SOAR-BYOI-Kaspersky
BYOI sample for Kaspersky endpoint security

By default, Cortex XSOAR by Palo Alto Networks (formerly Demisto) does not come with Integration of Kaspersky. I built a BYOI integration for Kaspersky based on the guide of Leonov (https://avleonov.com/2019/07/17/kaspersky-security-center-11-api-getting-information-about-hosts-and-installed-products/) using API to connect to KSC server.

In my integration sample, I made 2 Demisto commands: test-module and kasper-find-ip. With that:
1. The test-module is to test connection after creating a new integration in Demisto. It will shows Success or Failed after keying url & credential of KSC server.
2. The kasper-find-ip is to be used in War room playground or put in Playbook as an automated task. Its purpose is to get host information of an IP address.

Installation
1. Go to Cortex XSOAR (Demisto) GUI
2. Navigate to Setting > Integration > Select Upload Integration (the button with cloud and up arrow icon)
3. Select the Kasper.yml file
4. Done

Now you can edit/add more function to the integration yourself. Enjoy!
