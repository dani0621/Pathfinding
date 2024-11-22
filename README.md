# Machine Learning & AI Project 4: A* Pathfinding
## Danielle Li<br />November 22nd, 2024
<div align="center">
  <img width="450" alt="nbaLogo" src="https://github.com/user-attachments/assets/c5dbf1cf-d41c-473b-8682-8b880bf427ff">
</div>

### Literature Review/ Resources
As explained by [Tech With Tim's tutorial](https://www.youtube.com/watch?v=JtiK0DOeI4A&t=3846s), which I followed and adjusted for this project, at the base of A<sup>*</sup> Pathinfind Algorithms are nodes, which have letters starting from A, that we can visit, and they're connected to one another through edges. In this project, since I'm using a grid, the nodes are the corners of the grid and the edges connect them. There can also be weighted edges, but we use unweighted edges here because the distance between the nodes are the same since they're squares. The goal here to to find the shortest path from point A to point B using the edges in the grid. 

The heuristic function optimizes this function, allowing us to explore paths that we know are shorter and aren't extremely long. We use Manhattan distance or also known as L1 distance or taxicab distance, explained by [Datacamp](https://www.datacamp.com/tutorial/manhattan-distance),which measures the total "edge" cost of horizontal and vertical steps required to move from one point to another (up, down, left, right), like blocks in a city which is why it's called "Manhattan". It finds the absolutle differences between the nodes through these edges. Each step from one cell to an adjacent one increases the cost by 1.

<div align="center">
  <img width="300" alt="nbaLogo" src="https://github.com/user-attachments/assets/ce232c3e-9474-4054-a9d5-a717c83d1fec">
</div>

The is key in a grid where the cost to traverse each edge is the same. It's optimal because it never overestimates the true shortest path in a grid, and it's simple to compute because it only requires basic addition subtract, and absolute value operations. It usually provides a reasonable esitmate of the cost to reach the end node, prioritizing nodes that are likely on the optimal path. However, the Manhattan function is limited as it's not suitable for diagnol movement. If diagonal moves are allows, which it is not here, then Manhtattan distance would underestimate the cost as it doesn't traverse across diagonals. It also ignores obstacles as it assumes a clear path, so the path can be optimistic if there are many barriers.

I also used ChatGPT to debug my code, especially when installing libraries.

### Implementation
We installed pygame for our visualization tool. Tech With Tim originally had used a Spot class to check if the cell was a brrier, for drawing the spot, and for updating its neighbors. I used a 2D list or grid instead, where 0 represented empty cells and 1 represented a wall. This was better for my Pathinfindg algorithm because his original code drew the barriers, but for me, I was generating walls. I set that there was a 10% chance for a wall to generate for each cell, and so I didn't more complex functions like make_barrier. The colors I implmented where determined by if they were in the set of the path or visited where red represented exploration and the light blue color at the end showed the path. I also put a small animation selay by 0.01 to make visualization better.

We have an openset representd by  Priority Queue that keeps track of the nodes we want to look at next. We start by putting our start node along with the distance to the node within this openset. Then we use the following functions
* H(n) score gives an esimate of the distance from node n to the end node, and the H(n) we use here is the Manhattan Distance function
* G(n) score is the current shortest distance to get from the start node to this node
* F(n) score is then the estimate of how many blocks it will take from to get from the start node to this node and then from this node to the end node
  
Our algorithm looks at the different F score to see if we should consider different nodes to find a lower F-score (smallest distance estimate). In th beginning, all other nodes except for the start node has a distance of infinity from the start node because we haven't considered any paths. Then, we look at the neighbors of the first node, and we look at the length of the edge. We also make a guess for our H function, and we update our F score. Then, after this consideration, we put the f score of the node into the open set and continue this process for the neighbors. It checks up, down, left, right of the node we're on to see if they're barriers, and if they're not, they're added to a neighbors list. It continues checking the g-scores of the surrounding nodes to find the shortest f score. In the end, we use the smallest f-score in the open set, and we take it out of the open set, which consequently ends the algorithm as we took the end node out of the algorithm.

### User Interaction
The following is how the program should be used:
* The first mouse click sets the start point and the second click sets the end point. Make sure to not click a wall
* Pressing 'R' generates a new random grid
* The start/end points are reset autmatocally after a path is found so you can continue setting start/end points on that grid or create a new one

### Future Work
An edge case that I do want to wrok on in the future is when the start or end point is palced on a wall. Right now, the program is allowed to run so it continues exploring the whole grid, but I want to make it so that the user can't click set a wall as their start/end point.


