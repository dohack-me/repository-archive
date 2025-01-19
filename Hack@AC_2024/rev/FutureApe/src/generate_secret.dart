import 'dart:io';

void main() {
  String originalFlag = getOriginalFlag();
  List<int> encryptedFlag = encryptWithAffineCipher(originalFlag);
  saveToSecretFile(encryptedFlag);
}

String getOriginalFlag() {
  // Read the original flag from "list.txt"
  String filePath = "list.txt";
  try {
    File file = File(filePath);
    String content = file.readAsStringSync();
    return content.trim();
  } catch (e) {
    print("Error reading file: $e");
    exit(1);
  }
}

List<int> encryptWithAffineCipher(String originalFlag) {
  int a = 5; // Affine cipher parameters
  int b = 7;
  List<int> encryptedFlag = [];

  for (int i = 0; i < originalFlag.length; i++) {
    int charCode = originalFlag.codeUnitAt(i);

    if (originalFlag[i].toUpperCase() == originalFlag[i]) {
      // Apply affine cipher to uppercase letters
      encryptedFlag.add((a * charCode + b) % 256);
    } else if (originalFlag[i].toLowerCase() == originalFlag[i]) {
      // Apply affine cipher to lowercase letters
      encryptedFlag.add((a * charCode + b) % 256);
    } else {
      // Keep non-alphabetic characters unchanged
      encryptedFlag.add(charCode);
    }
  }

  return encryptedFlag;
}

void saveToSecretFile(List<int> encryptedFlag) {
  String filePath = "secret.txt";
  File file = File(filePath);

  try {
    file.writeAsStringSync(encryptedFlag.join(', '));
    print("Encrypted flag saved to secret.txt");
  } catch (e) {
    print("Error writing to file: $e");
  }
}
