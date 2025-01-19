#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <cctype>

void decryptWord(const std::string& cipher, const std::unordered_map<int, char>& bookIndex) {
    std::istringstream cipherStream(cipher);
    std::string token;
    while (std::getline(cipherStream, token, ',')) {
        try {
            size_t pos;
            int index = std::stoi(token, &pos);
            if (pos == token.size() && index > 0) {
                auto it = bookIndex.find(index);
                if (it != bookIndex.end()) {
                    std::cout << it->second;
                } else {
                    // skip if index not found
                    std::cerr << "Error: Invalid index in cipher: " << index << std::endl;
                }
            } else {
                std::cout << token;
            }
        } catch (const std::invalid_argument& e) {
            std::cout << token;
        }
    }
}

int main() {
    std::ifstream bookFile("book.txt");
    if (!bookFile.is_open()) {
        std::cerr << "Error opening book.txt" << std::endl;
        return 1;
    }

    std::ostringstream bookTextStream;
    bookTextStream << bookFile.rdbuf();
    std::string bookText = bookTextStream.str();
    bookFile.close();

    // map to store index
    std::unordered_map<char, int> bookIndex;
    std::unordered_map<int, char> reverseBookIndex;

    int currentIndex = 1;
    for (char currentChar : bookText) {
        if (std::isalpha(currentChar) && bookIndex.find(std::toupper(currentChar)) == bookIndex.end()) {
            bookIndex[std::toupper(currentChar)] = currentIndex;
            reverseBookIndex[currentIndex] = std::toupper(currentChar);
            currentIndex++;
        }
    }

    std::ifstream outputFile("output.txt");
    if (!outputFile.is_open()) {
        std::cerr << "Error opening output.txt" << std::endl;
        return 1;
    }

    std::string encryptedFlag;
    std::getline(outputFile, encryptedFlag);
    outputFile.close();

    decryptWord(encryptedFlag, reverseBookIndex);
    std::cout << std::endl;

    return 0;
}
