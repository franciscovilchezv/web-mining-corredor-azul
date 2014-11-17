/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package read.csv;
import com.opencsv.CSVWriter;
import java.io.*;
/**
 *
 * @author BAÑON
 */
public class ReadCsv {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException{
        // TODO code application logic here
        String csv = "output.csv";
        CSVWriter writer = new CSVWriter(new FileWriter(csv));        
    try{
        FileInputStream fstream = new FileInputStream("input4.txt");
        PrintWriter out = new PrintWriter(new FileWriter("output4.csv"));
        // Get the object of DataInputStream
        DataInputStream in = new DataInputStream(fstream);
        BufferedReader br = new BufferedReader(new InputStreamReader(in));
        String strLine = "";
        int numLinea = 0; 
        String codigo="";
        String codigousuario="";
        String fecha="";
        String tweet="";
        //Read File Line By Line
        int contador = 0;
        while ((strLine = br.readLine()) != null)   {
            
            switch (contador){
                case 1:
                    codigo = strLine;
                    contador++;      
                    break;
                case 5:
                    String lista = strLine;
                    String parts[] = lista.split("\t");
                    codigousuario = parts[0];
                    try{
                        fecha = parts[2];
                    }catch(Exception e){
                        
                    }
                    contador++;      
                    break;
                case 14:
                    //tweet = strLine;
                    contador++;      
                    break;
                case 15:
                    while(!strLine.equals("FIN TWEET")){
                        tweet +=" " + strLine;
                        strLine=br.readLine();
                    }
                    contador = 0;      
                    break;
                default:
                    contador++;      
                    break;
            }                
                                      
            if(strLine.equals("FIN TWEET")){
            out.print(codigo);
            out.print("|");
            out.print(codigousuario);
            out.print("|");
            tweet = tweet.replaceAll("Ã©", "é");
            tweet = tweet.replaceAll("Ã­", "í");
            tweet = tweet.replaceAll("Ã³", "ó");
            tweet = tweet.replaceAll("Ã¡", "á");
            tweet = tweet.replaceAll("Ãº", "ú");
            tweet = tweet.replaceAll("Ã±", "ñ");            
            tweet = tweet.replaceAll("Ã‘", "Ñ"); 
            tweet = tweet.replaceAll("Ã‰", "É");
            tweet = tweet.replaceAll("Ã­", "Í");
            tweet = tweet.replaceAll("Ã“", "Ó");            
            tweet = tweet.replaceAll("Ãš", "Ú");
            tweet = tweet.replaceAll("Ã", "Á");
            
            out.print(tweet);
            tweet = "";
            out.print("||");
            out.print(fecha);
            out.print("|0|0|0");
            out.print("\n");
            numLinea++;
        }
            numLinea++;
        }
            out.close();
            in.close();
        }catch (Exception e){//Catch exception if any
            System.err.println("Error: " + e.getMessage());
        }
    
    }
    
}
