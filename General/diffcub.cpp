#ifdef compile_instructions
c++ -Wfatal-errors $0 -o $0.x && $0.x $@; exit
#endif
/* With the above lines
one can directly run the source file.
*/


#include<fstream>
#include<vector>
#include<sstream>
#include<cassert>
#include<iostream>
#include<iomanip> // setprecision
std::vector<double> read_den(std::string filename){
	std::ifstream ifs(filename.c_str());
	std::string line;
	getline(ifs, line);
	getline(ifs, line);

	int nat; {getline(ifs, line); std::istringstream iss_line(line); iss_line >> nat;}
	
	int nx, ny, nz;
	getline(ifs, line); {std::istringstream iss_line(line); iss_line >> nx;}
	getline(ifs, line); {std::istringstream iss_line(line); iss_line >> ny;} 
	getline(ifs, line); {std::istringstream iss_line(line); iss_line >> nz;}

	for(int i = 0; i != nat; ++i){
		getline(ifs, line);
	}
	std::vector<double> v; v.reserve(nx*ny*nz);
	for(int i = 0; i != nx*ny*nz; ++i){
		double val; ifs >> val;
		v.push_back(val);
	}
	return v;
}

int main(int argc, char* argv[]){
	assert(argc == 4);
	std::string filename_ref = argv[1];
	std::string filename     = argv[2];
	std::string out          = argv[3];
	std::vector<double> ref = read_den(filename_ref);

	std::cout << "reference: " << filename_ref << std::endl;
	std::cout << "current: " << filename << std::endl;
	std::cout << "diff (curr - ref): " << out << std::endl;

	std::ifstream ifs(filename.c_str());
	std::ofstream ofs(out.c_str());

	std::string line;
	getline(ifs, line); ofs << line << '\n';
	getline(ifs, line); ofs << line << '\n';

	int nat; {getline(ifs, line); std::istringstream iss_line(line); iss_line >> nat; ofs << line << '\n';}
	
	int nx, ny, nz;
	getline(ifs, line); {std::istringstream iss_line(line); iss_line >> nx; ofs << line << '\n';}
	getline(ifs, line); {std::istringstream iss_line(line); iss_line >> ny; ofs << line << '\n';} 
	getline(ifs, line); {std::istringstream iss_line(line); iss_line >> nz; ofs << line << '\n';}

	for(int i = 0; i != nat; ++i){
		getline(ifs, line); ofs << line << '\n';
	}
	std::vector<double> curr = read_den(filename);
	assert(curr.size() == ref.size());
	ofs << std::setprecision(5) << std::scientific << std::showpos << std::setfill ('0') << std::setw(8);
	for(int i = 0; i != nx*ny*nz; ++i){
		ofs << curr[i] - ref[i] << ' ';
		if((i+1)%6==0) ofs << '\n';
	}
	std::cout << "done" << std::endl;
}

