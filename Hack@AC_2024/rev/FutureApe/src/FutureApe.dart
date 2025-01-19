import 'dart:convert';
import 'dart:io';

final List<int> secret = getSecret();
final List<int> decryptedFlag = decryptWithAffineCipher(secret);

void main() {
  print('''           ."`".
       .-.／ _=_ ＼.-.
      {   (,(oYo),)  }}
      {{  |   "   |  }}
      {{  ＼(---)／  }}
      {{   }'-=-'{  } }
      { {  }._:_.{   }}
      {{   } -:- {  } }
      {_{  }`===`{   _}
     (((())       (())))''');

  print("\ngive flag: ");
  List<int> input = stdin.readLineSync(encoding: latin1)!.codeUnits;

  // Check immediately without comparing the length
  bool correct = true;
  int minLength =
      input.length < decryptedFlag.length ? input.length : decryptedFlag.length;

  for (int i = 0; i < minLength; i++) {
    if (input[i] != decryptedFlag[i]) {
      correct = false;
      break;
    }
  }

  if (correct) {
    print("correct");
  } else {
    print("wrong");
  }
}

List<int> getSecret() {
  String filePath = "secret.txt";
  try {
    File file = File(filePath);
    String content = file.readAsStringSync();
    List<String> numbers = content.trim().split(', ');
    return numbers.map((e) => int.parse(e)).toList();
  } catch (e) {
    print("Error reading file: $e");
    exit(1);
  }
}

List<int> decryptWithAffineCipher(List<int> encryptedFlag) {
  int a = 5; // Affine cipher parameters
  int b = 7;
  int modInverseA = findModularInverse(
      a, 256); // Finding modular multiplicative inverse of 'a'

  List<int> decryptedFlag = [];

  for (int i = 0; i < encryptedFlag.length; i++) {
    // Apply inverse affine cipher
    decryptedFlag.add((modInverseA * (encryptedFlag[i] - b + 256) % 256));
  }

  return decryptedFlag;
}

int findModularInverse(int a, int m) {
  for (int i = 0; i < m; i++) {
    if ((a * i) % m == 1) {
      return i;
    }
  }
  return -1; // No modular inverse exists
}
