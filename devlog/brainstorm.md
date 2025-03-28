# Components

- agent
- algorithms
  - planning? model-based?
  - MCTS? prior knowledge?
- game/state
  - test environment
  - rules
  - progression/generalization
- visualization
  - How to visualize policy?
- evaluation

## Game/State

- grid for world map
- rules maintained on the side
- how to update rules?
  - incrementally, whenever a block is moved?
  - globally, by searching over board?
- store rule tokens in class param, iterate over them, check for adjacency

  - want to quickly check for rule configurations
  - store locations of each token
  - for each token, form its rule set

    - recursively check surrounding

  - since rules are read form left to right and top down, can just chec rows/cols linearly
  -

- do tiles have properties (such as STOP, inherited form objects), or only objects?
    - if only objects, then have to search tile for a HOT object to know if a MELT object will melt, whereas if tiles have properties, this is known directly from the tile attributes
    - but the tile attributes would have to be updated whenever objects move, whereas this is not the case for object attributes.

- time step:
    - [x] read rules
    - [ ] process movement
        - [ ] check for possiblity of movement (depends on current rules
        - [ ] move objects
            - [ ] update object positions
            - [ ] update board
    - [x] read rules
    - [ ] apply changes
        - [ ] if a MELT object is on a HOT tile, remove MELT object


## Connecting Board with Env

Env API provides:
    - step
    - reset
    - render
    - close
most important is step
    - input: action
    - returns: observation, next state, reward, termination/truncation
