#include <map>
#include <cmath>
#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <algorithm>
using namespace std;

int main()
{
	freopen("rank","r",stdin);
	int rpos=0;
	map<string,int> m;
	m.clear();
	string str[4000];
	while(cin>>str[rpos])
	{
		m[ str[rpos] ] ++;
		rpos++;
	}
	fclose(stdin);
	freopen("rankend.txt","w",stdout);
	for(map<string,int>::iterator it=m.begin();it!=m.end();it++)
	{
		cout<<it->first<<endl;
	}	
	fclose(stdout);
	return 0;
}
