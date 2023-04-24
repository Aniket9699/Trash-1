I would like to provide an update on the recent WebLogic patching activity that was completed successfully. However, there are some open points that I would like to bring to your attention for further discussion and resolution.

1. Standard Naming Convention for Start/Stop Scripts:
	As previously informed, we had requested for the start/stop scripts to follow a standard naming convention to facilitate automation.

2. Applying patch on Master and Slave Servers:
	The patch needs to be applied on both the WebLogic master and slave servers. On the master server, we need to start/stop the Admin, Node Manager, and JVM. On the slave server, we only need to stop and start the Node Manager and JVM.

3. Handling Different WebLogic Home Paths:
	Due to variations in the WebLogic Home path for some applications, we request to keep a single "weblogic.property" file in the path "/weblogic/script" where our scripts will be stored. This will help overcome the challenge of different WebLogic Home paths and ensure consistency in our deployment scripts.

In addition to the WebLogic patching activity, I would also like to share the proposed flow for OHS (Oracle HTTP Server) deployment as follows:

OHS Deployment Flow:

1. Stop the OHS components.
2. Stop the Node Manager.
3. Take a backup of the "wlserver" and "Opatch" servers.
4. Move the updated file and apply the patch.
5. If any errors occur during patch application, perform a rollback.
6. Start the Node Manager.
7. Start the OHS components.
8. Please review and confirm if the proposed OHS deployment flow aligns with your expectations. We also request for the deployment document for OHS deployment, including the necessary deployment commands.

Please note that due to server access issues, we were unable to complete OHS deployment testing. We have reached out to the PIM team to resolve this matter. In the meantime, we will be working on the OHS configuration and improving the current deployment flow.
