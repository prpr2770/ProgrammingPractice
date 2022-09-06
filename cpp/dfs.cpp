#include <iostream>
#include <vector>
#include <list>

using namespace std;


struct Edge{
    int src; 
    int dest;
};

class Graph{
    public: 
        // representing Graph with Adjacency-List(instead of AdjMatrix)
        vector< vector<int> > adjList; 
        int num_nodes;
        int num_edges; 
        vector<bool> visited;  // Set of VisitedNodes during traversal

        //
        Graph(vector<Edge> const &edges, int n, bool isDirected){
                num_nodes = n; 
                num_edges = edges.size();


                adjList.resize(n); // vector api

                for (auto &edge: edges){
                    adjList[edge.src].push_back(edge.dest); // vector-api
                    if(!isDirected){
                        // for undirected graph
                        adjList[edge.dest].push_back(edge.src);
                    }
                } 
        }

        void addEdge(int v1, int v2, bool isDirected){
                adjList[v1].push_back(v2);
                if(!isDirected){
                    adjList[v2].push_back(v1);
                };
        }

        void printGraph(){
            for(int i=0; i<num_nodes; i++){
                std::cout<< i << "-->";
                for(auto &v:adjList[i]){
                    std::cout<<v<<" ";
                }
                std::cout<<std::endl;
            }
        }


        void dfsUtil(int start_node){
            visited[start_node] = true;
            std::cout << start_node<< " ";

            for(auto &nbr: adjList[start_node]){
                if(!visited[nbr]){
                    dfsUtil(nbr);
                }
            };

        }

        void dfsTraversal(int start_node){

            // implemented recursively!
            visited.resize(num_nodes, false);


            std::cout<<"dfs traversal:";

            // Implicitly use the STACK of the Program
            // Do not have to explicitly define a stack-for code. 
            // Stack for DFS: 
            visited[start_node] = true; 
            std::cout<< start_node << " ";

            for(auto &nbr: adjList[start_node]){
                if(!visited[nbr]){
                    dfsUtil(nbr);
                }
            };

            std::cout<<std::endl;

        }

        void bfsTraversal(int start_node){
            int curr_node; 
            visited.resize(num_nodes,false);

            std::cout<<"bfs traversal: ";

            //Queue for BFS : Can be implemented using any container. 
            list<int> queue; 

            // Mark current node as visited and enqueue it; 
            visited[start_node] = true; 
            queue.push_back(start_node);

            while(!queue.empty()){
                curr_node = queue.front();
                std::cout<< curr_node << " ";
                queue.pop_front();

                for(auto &nbr:adjList[curr_node]){
                    if(!visited[nbr]){
                        visited[nbr] = true;
                        queue.push_back(nbr);
                    }
                };
            };

            std::cout<<std::endl;

        }

        void biDirectionalSearch(int n1, int n2){};

};

int main(){
    int n = 6; 
    vector<Edge> edges = { {0,1}, {1,2}, {2,0} , {2,1}, {3,2} , {4,5}, {5,4}};
    int n1=0, n2=0;

    Graph graph(edges, n, true);
    graph.printGraph();

    graph.dfsTraversal(n1);
    graph.bfsTraversal(n2);
    graph.biDirectionalSearch(n1, n2);

    return 0; 


}