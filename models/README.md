Models
1:
    Convolutional(filters: 16, window: 3x3, stride:1, activation: relu)
    MaxPooling(2x2)
    Convolutional(filters: 32, window: 3x3, stride:1, activation: relu)
    MaxPooling(2x2)
    Convolutional(filters: 64, window: 3x3, stride:1, activation: relu)
    MaxPooling(2x2)
    Flatten
    Dense(nodes: 64, activation: relu)
    Dense(nodes: 128, activation: relu)
    Dense(nodes: 256, activation: relu)
    Dense(nodes: 128, activation: relu)
    Dense(nodes: 1, activation: none)