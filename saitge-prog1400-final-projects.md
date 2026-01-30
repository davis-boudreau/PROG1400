#### **Games and Their OOP Principles**

| **Game**                   | **Encapsulation**                     | **Aggregation**                               | **Inheritance**                   | **Polymorphism**                            | **Abstraction / Interface**  | **Inner Classes**                  |
| -------------------------- | ------------------------------------- | --------------------------------------------- | --------------------------------- | ------------------------------------------- | ---------------------------- | ---------------------------------- |
| **Guess the Number**       | Game logic hidden in `Game` class     | Minimal                                       | Variants (timed mode)             | Different input strategies                  | Abstract `play()` method     | None                               |
| **Tic-Tac-Toe**            | Board state in `Board` class          | `Game` uses `Board` + `Player`                | `HumanPlayer` vs `AIPlayer`       | `makeMove()` overridden                     | `MoveStrategy` interface     | `Cell` inside `Board`              |
| **Rock-Paper-Scissors**    | Choice/result logic in `Game`         | Players aggregated                            | Extended rules inherit base       | AI strategies override                      | Abstract `determineWinner()` | None                               |
| **Hangman**                | Word & guess logic in `HangmanGame`   | `Word` + guessed letters                      | Multiplayer/timed versions        | Difficulty changes word selection           | Abstract `selectWord()`      | `Guess` inside `HangmanGame`       |
| **Memory Match**           | Card flip logic in `Card` class       | `GameBoard` holds cards                       | Different board sizes/themes      | Shuffle algorithms vary                     | `ShuffleStrategy` interface  | `Position` inside `GameBoard`      |
| **Snake Game**             | Movement/collision in `Snake`         | `Game` aggregates `Snake`, `Food`, `Board`    | Snake types inherit base          | Movement logic overridden                   | `Drawable` interface         | `Segment` inside `Snake`           |
| **Simple RPG Battle**      | Stats & combat in `Character`         | `Battle` uses `Player` + `Enemy`              | `Warrior`, `Mage` subclasses      | Different `attack()` methods                | Abstract `performAction()`   | `InventoryItem` inside `Character` |
| **Connect Four**           | Board state in `Board` class          | `Game` uses `Board` + `Player`                | Variants for grid size            | AI strategies differ                        | Abstract `checkWinner()`     | `Cell` inside `Board`              |
| **Maze Runner**            | Maze generation in `Maze`             | `Game` uses `Maze`, `Player`, `Obstacle`      | Different maze types inherit base | Movement algorithms vary                    | `Movable` interface          | `Cell` inside `Maze`               |
| **Pac-Man** *(Case Study)* | Ghost AI & Pac-Man logic encapsulated | `Game` aggregates `PacMan`, `Ghosts`, `Board` | Ghost types inherit base `Ghost`  | Different ghost behaviors override `move()` | Abstract `GameEntity` class  | `Tile` inside `Board`              |

***

#### **Real-World Applications and Their OOP Principles**

| **Application**               | **Encapsulation**                                | **Aggregation**                                    | **Inheritance**                           | **Polymorphism**                                                 | **Abstraction / Interface**           | **Inner Classes**                    |
| ----------------------------- | ------------------------------------------------ | -------------------------------------------------- | ----------------------------------------- | ---------------------------------------------------------------- | ------------------------------------- | ------------------------------------ |
| **Library Management System** | `Book`, `Member` classes hide internal data      | `Library` aggregates books and members             | Specialized `DigitalBook` inherits `Book` | Different search strategies override `search()`                  | Abstract `Item` class for books/media | `LoanRecord` inside `Member`         |
| **Employee Management Tool**  | Employee details hidden in `Employee` class      | `Department` aggregates employees                  | `Manager` inherits `Employee`             | Different payroll calculations override `calculatePay()`         | Interface for `Payable` entities      | `Address` inside `Employee`          |
| **Online Shopping Cart**      | Cart logic inside `Cart` class                   | `Order` aggregates products                        | `DiscountedProduct` inherits `Product`    | Different payment methods override `processPayment()`            | Abstract `PaymentMethod` class        | `CartItem` inside `Cart`             |
| **Event Management System**   | Event details encapsulated in `Event` class      | `Event` aggregates `Attendee`, `Venue`, `Schedule` | `ConferenceEvent` inherits `Event`        | Different ticket pricing strategies override `calculatePrice()`  | Interface for `Notifiable`            | `ScheduleItem` inside `Schedule`     |
| **Student Grade Tracker**     | Grades stored in `Grade` class                   | `Course` aggregates students and grades            | `GraduateStudent` inherits `Student`      | Different grading policies override `computeGrade()`             | Abstract `Person` class               | `Assignment` inside `Course`         |
| **Hotel Reservation System**  | Reservation logic inside `Booking` class         | `Hotel` aggregates rooms and bookings              | `SuiteRoom` inherits `Room`               | Different pricing models override `calculateRate()`              | Interface for `Reservable`            | `PaymentDetail` inside `Booking`     |
| **Bank Account Management**   | Account details hidden in `Account` class        | `Customer` aggregates accounts                     | `SavingsAccount` inherits `Account`       | Different transaction types override `processTransaction()`      | Abstract `Account` class              | `TransactionRecord` inside `Account` |
| **Car-Pool Service**          | Ride details encapsulated in `CarPoolRide` class | `CarPoolRide` aggregates `Driver` and `Passenger`  | `PremiumDriver` inherits `Driver`         | Different fare calculation strategies override `calculateFare()` | Interface for `LocationAware`         | `Location` inside `CarPoolRide`      |

***

If we consider **Pac-Man’s OOP principles**—such as **Encapsulation**, **Aggregation**, **Inheritance**, **Polymorphism**, and **Abstraction**—then similar games would be those that:

*   Use **entities with distinct behaviors** (e.g., player, enemies, items).
*   Have **hierarchies for characters or objects** (e.g., different enemy types).
*   Implement **interfaces or abstract classes** for common behaviors (e.g., movable, drawable).
*   Use **collections** for managing multiple objects (e.g., pellets, obstacles).
*   Possibly include **inner classes** for tightly coupled components (e.g., grid cells, map tiles).

***

### ✅ **Games Similar to Pac-Man in OOP Design**

1.  **Ms. Pac-Man**
    *   Same core structure as Pac-Man but with enhanced AI and maze variations.
    *   Similar class hierarchy for ghosts and player.

2.  **Bomberman Series**
    *   Classes for Player, Bomb, Wall, Power-up.
    *   Inheritance for different bomb types and player abilities.
    *   Aggregation for grid and items.

3.  **Lock ’n’ Chase**
    *   Maze-based chase game with police AI.
    *   Similar entity design: Player, Enemy, Collectibles.

4.  **Lady Bug**
    *   Rotating gates add complexity but still uses maze navigation.
    *   Classes for gates, player, enemies.

5.  **Dig Dug**
    *   Maze/tunnel system with enemies and player.
    *   Inheritance for different enemy behaviors.

6.  **Pengo**
    *   Pushable blocks and enemies.
    *   Classes for Player, Block, Enemy; polymorphism for block interactions.

7.  **Forget Me Not** (Indie)
    *   Roguelike maze game with shooting mechanics.
    *   Interfaces for movable and shootable entities.

8.  **Pac-Man Championship Edition**
    *   Modernized Pac-Man with dynamic mazes.
    *   Same OOP principles but extended for timed sessions and new modes.

***

### ✅ **Why These Games Are Similar in OOP Terms**

*   **Encapsulation**: Each game object (player, enemy, item) manages its own state.
*   **Aggregation**: Game class holds collections of entities (ghosts, pellets, bombs).
*   **Inheritance**: Different enemy types or power-ups extend base classes.
*   **Polymorphism**: Common methods like `move()` or `update()` behave differently for each entity.
*   **Abstraction**: Interfaces for rendering, collision detection, and movement.
*   **Inner Classes**: Often used for grid cells or map tiles.

***
