#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

int main() {

    const std::vector<std::string> bookLyrics = {
        "God save our gracious King!",
        "Long live our noble King!",
        "God save the King!",
        "Send him victorious,",
        "Happy and glorious,",
        "Long to reign over us:",
        "God save the King!",
        "",
        "Thy choicest gifts in store,",
        "On him be pleased to pour;",
        "Long may he reign:",
        "May he defend our laws,",
        "And ever give us cause,",
        "To sing with heart and voice,",
        "God save the King!"
    };


    std::ostringstream bookTextStream;
    for (const std::string& line : bookLyrics) {
        bookTextStream << line;
    }
    std::string bookText = bookTextStream.str();


    std::ofstream bookFile("book.txt");
    if (!bookFile.is_open()) {
        std::cerr << "Error opening book.txt" << std::endl;
        return 1;
    }

    bookFile << bookText;
    bookFile.close();

    return 0;
}
