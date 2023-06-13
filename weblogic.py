cd /home/aniket
echo "This Server have below mentioned domains."
echo "--------------------------------------------------"
# Read each line from the file and print it
while IFS= read -r line; do
  URL=$(echo "$line" | cut -d',' -f1)
  MachineName=$(echo "$line" | cut -d',' -f2)
  echo "URL = $URL and Machine Name = $MachineName"
  # create start script
  cat /home/aniket/Oracle/products/Oracle_Home/oracle_common/common/bin/start_weblogic.py > /home/aniket/Start_$MachineName.py
  cat /home/aniket/Oracle/products/Oracle_Home/oracle_common/common/bin/get_node_by_node_name.py > /home/aniket/Stop_$MachineName.py
  # Replace the URL and machine name in the script file
  cd /home/aniket
  sed -i "s|t3://localhost:7001|$URL|g; s|Machine-0|$MachineName|g" Start_$MachineName.py
  sed -i "s|t3://localhost:7001|$URL|g; s|Machine-0|$MachineName|g" Stop_$MachineName.py
  echo "==============================================================================================================="
  cat Start_$MachineName.py
  echo "==============================================================================================================="
  cat Stop_$MachineName.py
  echo "==============================================================================================================="
done < Weblogic.txt
echo "--------------------------------------------------"


while IFS= read -r line; do
  URL1=$(echo "$line" | cut -d',' -f1)
  MachineName1=$(echo "$line" | cut -d',' -f2)
  echo "-------------------------------------------------------------------------------------------------------------"
  echo "URL = $URL1 and Machine Name = $MachineName1"
  echo "--------------------------------------------------------------------------------------------------------------"
  sh /home/aniket/Oracle/products/Oracle_Home/oracle_common/common/bin/wlst.sh /home/aniket/Stop_$MachineName1.py
  echo "--------------------------------------------------------------------------------------------------------------"
  sh /home/aniket/Oracle/products/Oracle_Home/oracle_common/common/bin/wlst.sh /home/aniket/Start_$MachineName1.py
  echo "-------------------------------------------------------------------------------------------------------------"
done < Weblogic.txt
