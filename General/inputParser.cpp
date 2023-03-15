#ifdef compile_instructions
g++ -std=c++17 -Wfatal-errors $0 -o $0.x && $0.x $@; exit
#endif
/* With the above lines
one can directly run the source file.
*/



/*
 * c++ program to parse input parameters
 * from a loosely formatted text file.
 * Rafi Ullah, UCSC, Santa Cruz
 * March 08, 2023
 *
 */
#include <fstream>
#include <iostream>
#include <string>
#include <sstream>
#include <map>
#include <iomanip>
using namespace std;

// trim each line of the input file
string trim(string s)
{
        s.erase(0, s.find_first_not_of(" "));
    // trim everything from the start of the line to the first charachter in the line
        s.erase(s.find_last_not_of(" \n\r\t") + 1);
    // trim everything from the last character to the end of the line.
    return s;
}

map<string, string> input_parser (fstream& fin)
{
    map<string, string> dict;
        bool b_join = false;
        bool b_joined = false;
        bool b_will_join = false;
        string key_word = "";
        for (string line; getline(fin, line);)
    {
        b_will_join = false;
                b_joined = false;
                string line2 = trim(line);

        //Skip comment line
                if (line[0] == '#') continue;
        // Skip inline comment
        line2.assign(line2.substr(0,line.find('#')));

                //Remove "\"
                if (line2[line2.length() - 1] == '\\')
        {
                        b_will_join = true;
                        line2[line2.length() - 1] = ' ';
                }

                if (b_join)
        {
                        dict [key_word] += " " + line2;
                        b_joined = true;
                }
                b_join = b_will_join;

                if (!b_joined)
        {
                        size_t equalpos = line2.find('=');
                        if (equalpos == string::npos) continue;
                        key_word = trim(line2.substr(0, equalpos - 1));
                        dict[key_word] = trim(line2.substr(equalpos + 1, line2.length() - equalpos - 1));
                }
        }
        return dict;
}

int main(int argc, char** argv)
{
    string inFile = "";
    fstream fin;

    if (argc == 1)
    {
        inFile = "param.in";
        cout << "Input file not specified at runtime." <<endl;
        cout << "Attempting to read simulation parameters from default input file: " << inFile <<endl;
        fin.open(inFile, ios::in);
        if (fin.fail())
        {
            cout << "ERROR :: input file "<< inFile << " does not exist." <<endl;
            exit(EXIT_FAILURE);
        }
        cout << "Found the default input file: " << inFile << endl;
        cout << "Reading simulation parameters from input file: " << inFile << endl;

    }

    else if ( argc == 2 )
    {
        inFile = argv[1];
        cout << "Attempting to read simulation parameters from specified input file: " << inFile << endl;
        fin.open(inFile, ios::in);
        if (fin.fail())
        {
        cout << "ERROR :: input file "<< inFile << " does not exist." <<endl;
        exit(EXIT_FAILURE);
        }
        cout << "Found the input file: " << inFile << endl;
        cout << "Reading simulation parameters from input file: " << inFile<<endl;
    }
    else if (argc > 2)
    {
        cout << "ERROR: too many arguments." <<endl;
        cout << "Usage: ./dmd inputFile"  << endl;
        exit(EXIT_FAILURE);
    }

    map<string, string> input_dict  = input_parser (fin);
    for (const auto& [key, value] : input_dict)
        cout << "key word = " << setw(40) << left << key<<"       value = " << value <<endl;
    return 0;
}
