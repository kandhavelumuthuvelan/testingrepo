import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.KeyGenerator;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import org.apache.commons.codec.binary.Base64;
class patdecryptor
{
public static void main(String args[])
{
	 try {
	 String decryptedMessage="";
	//byte[]  encryptedMessage = "aZ+kQeh+oRt3t7QJLg1ekRDtXSt+IOO/e10/KjQnpoZt+jDcMgzz3c6dBuYxG57WvTCxjkFYThA=".getBytes();
	//byte[]  aKey="8h+uDhVYsMh5f+nsqyPWqEpr/ptitc1k".getBytes();
	byte[]  encryptedMessage=args[0].getBytes();
	byte[]  aKey=args[1].getBytes();
	
     
         byte[] encodedKey = Base64.decodeBase64(aKey);
         SecretKey key = new SecretKeySpec(encodedKey, 0, encodedKey.length, "DESede");
         Cipher decipher = Cipher.getInstance("DESede");
         decipher.init(2, key);
         byte[] messageToDecrypt = Base64.decodeBase64(encryptedMessage);
         byte[] decryptedBytes = decipher.doFinal(messageToDecrypt);
         decryptedMessage = new String(decryptedBytes);
         System.out.print(decryptedMessage);
     }
	 catch (NoSuchPaddingException | InvalidKeyException | IllegalBlockSizeException | BadPaddingException | NullPointerException | IllegalArgumentException | NoSuchAlgorithmException var8) {
         System.out.println("Cannot decrypt this message\n" + var8.getMessage());
      }
}
}