#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <unordered_map>


void encryptWord(const std::string& word, const std::unordered_map<char, int>& bookIndex, std::ofstream& outputFile) {
    for (char currentChar : word) {
        if (std::isalpha(currentChar)) {
            int index = bookIndex.at(std::toupper(currentChar));
            outputFile << index << ",";
        } else {
            outputFile << currentChar;
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


    std::unordered_map<char, int> bookIndex;


    int currentIndex = 1;
    for (char currentChar : bookText) {
        if (std::isalpha(currentChar) && bookIndex.find(std::toupper(currentChar)) == bookIndex.end()) {
            bookIndex[std::toupper(currentChar)] = currentIndex++;
        }
    }


    std::ifstream flagFile("flag.txt");
    if (!flagFile.is_open()) {
        std::cerr << "Error opening flag.txt" << std::endl;
        return 1;
    }

    std::string placeholderFlag;
    flagFile >> placeholderFlag;
    flagFile.close();


    std::ofstream outputFile("output.txt");
    if (!outputFile.is_open()) {
        std::cerr << "Error opening output.txt" << std::endl;
        return 1;
    }

    encryptWord(placeholderFlag, bookIndex, outputFile);

    outputFile.close();

    return 0;
}
