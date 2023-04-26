import java.security.cert.TrustAnchor
import java.sql.Connection
import javax.net.ssl.SSLContext
import groovy.json.JsonSlurper
import javax.net.ssl.HostnameVerifier
import javax.net.ssl.HttpsURLConnection
import javax.net.ssl.SSLContext
import javax.net.ssl.TrustManager
import javax.net.ssl.X509TrustManager
import java.io.OutputStream
import groovy.json.*
import groovy.transform.Field

//Intiating varaibles
@Field def url = "https://ip:8443"
@Field def username = "admin"
@Field def password = "password"
@Field def ApplicationName = "JBOSS_TEST_30.43"
@Field def UserName = "root"
@Field def CurrentAgentUser = "${p:agent/USER}"
//Encoding username and password
@Field String encoding = Base64.getEncoder().encodeToString(( username + ":" + password ).getBytes("UTF-8"));

def hostnames = "DTPL-LPT-47" 
//hostnames = hostnames.replace(".YESBANK.IN","").replace(".YESBANK.COM","")

//Method to retrieve Agents
def getAgents(){
    
    //API URL
    def uri = "https://192.168.30.43:8443/rest/agent?rowsPerPage=250&pageNumber=1&orderField=name&sortType=asc"
    
    // Create a StringBuilder to hold the data
    StringBuilder data = new StringBuilder()
    
    //Creating object to accept all hostnames
    def nullHostnameVerifier = [
        verify:{hostname, session -> true} 
    ]
    
    //Accept all certificate ignore SSL check
    def sc = SSLContext.getInstance("SSL")
    def trustAll = [getAcceptedIssuers: {}, checkClientTrusted: { a, b -> }, checkServerTrusted: { a, b -> }]
    sc.init(null, [trustAll as X509TrustManager] as TrustManager[], null);
    HttpsURLConnection.defaultSSLSocketFactory = sc.socketFactory;
    HttpsURLConnection.setDefaultHostnameVerifier(nullHostnameVerifier as HostnameVerifier);
    
    //Setting up connection
    def connection = new URL(uri).openConnection() as HttpURLConnection
    
    //Setting Headers
    connection.setRequestMethod("GET");
    connection.setRequestProperty("Accept", "application/json")
    connection.setRequestProperty("Authorization","Basic " + encoding)
     
    //println"===========================Response Headers============================================="
    Map<String, List<String>> map = connection.getHeaderFields();
    for(Map.Entry<String, List<String>> entry : map.entrySet()){
        //println"${entry.getKey()}:${entry.getValue()}"
    }
    //println"========================================================================================"
    
    if ( connection.responseCode == 200) {
        // get the JSON response
        json = connection.inputStream.withCloseable { inStream ->
                        new JsonSlurper().parse( inStream as InputStream )
        }
        //retrieve data from JSON
        for (entry in json) {
            // retrieve data from each entry
            println "________________________Agent Details___________________________________________"
            def name = entry.name
            def licenseType = entry.licenseType
            def status = entry.status
            def Ip=getAgentIpAndOsType(name,"ip")
            def OS=getAgentIpAndOsType(name,"sys.os.name")
            println "Adding ${name},${licenseType},${status},${Ip},${OS} into agent.txt file"
            println "_________________________________________________________________________________"
            data.append("$name,$licenseType,$status,$Ip,$OS\n")
        }
         
        // Write data to text file
        File file = new File("agents.txt")
        file.write(data.toString())
        println "Data written to agents.txt successfully."
    }else if(connection.responseCode == 404){
        //Do nothing
    }else {
        //Do nothing
    }
}

// 
def getAgentIpAndOsType(String AgentName,String Property){
    
    //API URL
    def uri = "https://192.168.30.43:8443/cli/agentCLI/getProperty?agent=${AgentName}&name=${Property}"
    
    //Creating object to accept all hostnames
    def nullHostnameVerifier = [
        verify:{hostname, session -> true} 
    ]
    
    //Accept all certificate ignore SSL check
    def sc = SSLContext.getInstance("SSL")
    def trustAll = [getAcceptedIssuers: {}, checkClientTrusted: { a, b -> }, checkServerTrusted: { a, b -> }]
    sc.init(null, [trustAll as X509TrustManager] as TrustManager[], null);
    HttpsURLConnection.defaultSSLSocketFactory = sc.socketFactory;
    HttpsURLConnection.setDefaultHostnameVerifier(nullHostnameVerifier as HostnameVerifier);
    
    //Setting up connection
    def connection = new URL(uri).openConnection() as HttpURLConnection
    
    //Setting Headers
    connection.setRequestMethod("GET");
    connection.setRequestProperty("Accept", "text/plain")
    connection.setRequestProperty("Authorization","Basic " + encoding)
     
    //println"===========================Response Headers============================================="
    Map<String, List<String>> map = connection.getHeaderFields();
    for(Map.Entry<String, List<String>> entry : map.entrySet()){
        //println"${entry.getKey()}:${entry.getValue()}"
    }
   // println"========================================================================================"
    
    if ( connection.responseCode == 200) {
        // get the plain text response
        def inputStream = connection.inputStream
        def reader = new BufferedReader(new InputStreamReader(inputStream))
        def response = ''
        String line
        while ((line = reader.readLine()) != null) {
            response += line
        }
        reader.close()
        inputStream.close()

        //println "Response: ${response}"
        return response // Store response in a variable            
    }else if(connection.responseCode == 404){
        //Do nothing
    }else {
        //Do nothing
    }
}

getAgents()
