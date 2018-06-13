import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.security.spec.InvalidKeySpecException;

import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import javax.xml.bind.DatatypeConverter;


/**
* PasswordHelper provides easy to use methods to create and verify hashed and
* salted passwords.
*
* @author  Hans Goldman
* @version 1.0
* @since   2018-04-22
*/
public class PasswordHelper
{
    /**
     * Used when creating a new password for a user. Hashes and salts then
     * returns a string containing both.
     * 
     * @param passwordString The given password supplied by the user
     * @return A string containing both the salt and the hashed password
     */
    public static String createPassword(final String passwordString)
    {
        byte[] salt              = createSalt();
        String hashAndSaltString = hashPassword(passwordString, salt);

        return hashAndSaltString;
    }


    /**
     * Verifies whether a given password matches what is stored in the database.
     * 
     * @param givenPassword A string containing the password supplied by the user
     * @param storedPasswordString A string containing the password as stored on the server
     * @return True if the password matches what is in the database; otherwise false
     */
    public static boolean isPasswordValid(String givenPassword, String storedPasswordString)
    {
        boolean returnResult   = false;
        byte[] saltBytes       = getSaltBytesFromHex(storedPasswordString);
        String givenHashString = hashPassword(givenPassword, saltBytes);

        if(givenHashString.equals(storedPasswordString))
        {
            returnResult = true;
        }

        return returnResult;
    }


    /**
     * Creates a hex string from a given password and salt. Change iterations
     * value to something that takes about a half a second on the machine running
     * this code.
     * 
     * @param passwordString User supplied password string
     * @param salt The salt used for hashing the password
     * @return A string containing both the sale and the hashed password
     */
    private static String hashPassword(final String passwordString, final byte[] salt)
    {
        try
        {
            final char[] password = passwordString.toCharArray();
            final int iterations  = 100000;
            final int keyLength   = 256;

            SecretKeyFactory skf  = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA512");
            PBEKeySpec spec       = new PBEKeySpec(password, salt, iterations, keyLength);
            SecretKey key         = skf.generateSecret(spec);
            byte[] passwordHash   = key.getEncoded();

            String hashString     = toHexString(salt) + toHexString(passwordHash);

            return hashString;
        }
        catch(NoSuchAlgorithmException | InvalidKeySpecException e)
        {
            throw new RuntimeException(e);
        }
    }


    /**
     * Generated a cryptographically-secure random salt.
     * 
     * @return A cryptographically-secure random salt
     */
    private static byte[] createSalt()
    {
        SecureRandom random = new SecureRandom();
        byte[] salt         = new byte[64];

        random.nextBytes(salt);

        return salt;
    }


    /**
     * Converts byte array variables to hex strings.
     * 
     * @param bytes A byte array that you want the associated hex string for
     * @return A hex string representation of the given byte array
     */
    private static String toHexString(final byte[] bytes)
    {
        String hexString = DatatypeConverter.printHexBinary(bytes);

        return hexString;
    }


    /**
     * Parses a given hex string containing a salt and password hash and returns
     * the portion of the hex string that represents the salt.
     * 
     * @param hexString A string containing the salt and hash
     * @return A string containing just the salt
     */
    private static byte[] getSaltBytesFromHex(String hexString)
    {
        String saltString = hexString.substring(0, 128);
        byte[] bytes      = DatatypeConverter.parseHexBinary(saltString);

        return bytes;
    }


    /**
     * Parses a given hex string containing a salt and password hash and returns
     * the portion of the hex string that represents the hash.
     * 
     * @param hexString A string containing the salt and hash
     * @return A string containing just the hash
     */
    private static byte[] getHashBytesFromHex(String hexString)
    {
        String hashString = hexString.substring(128, 192);
        byte[] bytes      = DatatypeConverter.parseHexBinary(hashString);

        return bytes;
    }
}
