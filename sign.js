

const starkwareCrypto = require('@starkware-industries/starkware-crypto-utils');

try{
  var EthAddress = process.argv[3]
  var EthSignature = process.argv[2]

}
catch(e){
}

var privatekey=starkwareCrypto.keyDerivation.getPrivateKeyFromEthSignature(EthSignature)

starkkey=starkwareCrypto.keyDerivation.privateToStarkKey(privatekey)
var keyPair = starkwareCrypto.ec.keyFromPrivate(privatekey, 'hex')
msgHash=starkwareCrypto.pedersen(["UserRegistration:",EthAddress])

var msgSignature = starkwareCrypto.sign(keyPair, msgHash)
var {r, s} = msgSignature

var output= {'privatekey':privatekey, 'starkkey':'0x'+starkkey, 'r':'0x'+msgSignature.r.toJSON(), 's':'0x'+msgSignature.s.toJSON()}
console.log(JSON.stringify(output))