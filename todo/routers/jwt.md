jwt : 3 parts

header:payload:signature

header
payload
signature

1.  header : 2 parts
    "alg" : "hs256"
    "typ" : "jwt"

    it is then encoded into base 64 to form first part of jwt

2.  payload
    consists of data . payload data contains claims :3 types of claims
    Registered :

         -iss issuer(identifies the primcipal that issued the jwt),

         -sub subject (holds statements about subject) should be scoped locally or globally unique [id for jwt kindof],

         -exp : expiration time , not mandatory [recommended to set exp time, This is because if the token never expires, then anyone who has a JWT will be authorized by the server.]


         it is then encoded into base 64 to form second part of jwt

         public
         private

3.  signature :
    The JWT signature is created by using the algorithm in the header to hash out the encoded header encoded payload and secret.
    The secret can be anything but is saved somewhere on the server that the client does not have access to.
    The signature is the third and final part of a JWT.

    eg : hmcasha256(
    base64urlEncode(header)+"."+
    base64UrlEncode(payload),secret_key
    )
