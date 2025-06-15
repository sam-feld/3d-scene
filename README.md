# Project 3: Interactive (Billiard Table) Scene

## Authors
Aban Khan, Shmuel Feld, Matthew Glennon, Jose Salgado, Sai Srujan Vemula, Camryn Keller

## How to run
The main code is run from the `Room` class in `room.py`

## Consistency guidelines that we followed during development
- **Units**: When drawing our scene, one unit in the coordinate system will correspond to one foot
- **Models**: When creating hierarchical models, objects will be centered along the x and z axes, positioned above the ground level, as if they’re placed on the floor at the y = 0 plane, as shown in the image below.
![demopnstration](https://github.com/user-attachments/assets/562dd0e4-c9a5-4814-aefc-b15df373a29a)
- **Style**: We'll follow standard Python style conventions. Here are some standard Python style guidelines:

    | Element               | Naming Convention | Example                                    |
    |-----------------------|-------------------|--------------------------------------------|
    | **File, Variable, and Function Names** | `snake_case`      | `data_loader.py`, `user_name`, `process_data()` |
    | **Class Names**       | `CamelCase`       | `DataProcessor`, `UserAccount`             |
    | **Constants**         | `ALL_CAPS`        | `MAX_SIZE`, `DEFAULT_TIMEOUT`              |

- **Animation**: We can animate items separately by incrementing separate frame counters for each animated element. When an animation is active, the corresponding frame counter is incremented to create motion over time. Here's an example:

    ```python
    def animation():
        global animate_dice, dice_frame, animate_eight_ball, eight_ball_frame
        if animate_dice:
            dice_frame += 1
        if animate_eight_ball:
            eight_ball_frame += 1
    ```
- **Applying Materials**: Applying materials in the scene is simple. Just use a line like `Materials.set_material(GL_FRONT, Materials.COPPER)` before drawing an object to set its material properties. This material will be applied to all objects drawn afterward until a new material is set. You’ll find plenty of predefined materials in the `Materials` class (like `Materials.SILVER` or `Materials.GOLD`), and you can add your own custom materials there if you want.

- **Applying Textures**: Applying textures to objects in the scene is straightforward once the textures are loaded. Simply use a line like `Textures.set_texture(texture_name)` before drawing an object to set its texture properties. This texture will be applied to all objects drawn afterward until a new texture is set. Keep in mind that initializing and loading textures into the project can be more complex. This instruction is specifically for already loaded textures. If you want to add a new texture to the project, speak to Sam or Jay.
