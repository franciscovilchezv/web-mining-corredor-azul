/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package verifytweetwithdictionary;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 *
 * @author BAÑON
 */
public class VerifyTweetWithDictionary {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        
        try {
 
            FileInputStream fstream = new FileInputStream("output.csv");
            PrintWriter outCorrectos = new PrintWriter(new FileWriter("output_c.csv"));
            PrintWriter outIncorrectos = new PrintWriter(new FileWriter("output_i.csv"));
            
            DataInputStream in = new DataInputStream(fstream);
            BufferedReader br = new BufferedReader(new InputStreamReader(in));
            String strLine = ""; 
            int contador = 0;
            while ((strLine = br.readLine()) != null)   {
                
                String parts[] = strLine.split("\\|");
		String tweet = parts[3];
                String parts2[] = tweet.split(" ");
                boolean val;
                val = true;
                for (String i : parts2) {
                    val = val && hallaTermino(i);
                }
                if(val){
                    outCorrectos.print(strLine);
                    outCorrectos.print("\n");
                }else{
                    outIncorrectos.print(strLine);
                    outIncorrectos.print("\n");
                }
                contador++;
                System.out.println(contador);
            }
            
            outCorrectos.close();
            outIncorrectos.close();
            in.close();
 
	  } catch (Exception e) {
 
		e.printStackTrace();
 
	  }
        
    }
    
    public static boolean hallaTermino(String valor){
        boolean flag = true;
        try{
            String termino = valor;
            System.out.println(valor);
            String path = "http://www.spanishcentral.com/translate/" + termino;
            URL url = new URL(path);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Accept", "application/json");
 
            if (conn.getResponseCode() != 200) {
                throw new RuntimeException("Failed : HTTP error code : "+ conn.getResponseCode());
            }
            BufferedReader br = new BufferedReader(new InputStreamReader((conn.getInputStream())));
            String output ="";
            String gg;
            while ((gg = br.readLine()) != null) {
                output += gg;
            }
            if(output.contains("definition single-definition")){
                flag = true;
                System.out.println("Correcto");
            }else{
                flag = false;
                System.out.println("Incorrecto");
            }
            conn.disconnect();
        }catch(Exception e){
            System.out.println(e.toString());
        }        
        return flag;
    }
    
}
