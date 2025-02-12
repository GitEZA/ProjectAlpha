import unreal
import json
import os

# 出力フォルダ
output_dir = os.path.join(unreal.Paths.project_saved_dir(), "GridExport")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# グリッド設定
grid_size = 10000  # グリッドの大きさ（UEのユニット）
level = unreal.EditorLevelLibrary.get_editor_world()

# すべてのアクターを取得
actors = unreal.EditorLevelLibrary.get_all_level_actors()

# グリッドごとに情報を分類
grid_data = {}

for actor in actors:
    location = actor.get_actor_location()
    grid_x = int(location.x // grid_size)
    grid_y = int(location.y // grid_size)

    grid_key = f"{grid_x}_{grid_y}"

    if grid_key not in grid_data:
        grid_data[grid_key] = {"actors": []}

    actor_info = {
        "name": actor.get_name(),
        "class": actor.get_class().get_name(),
        "location": [location.x, location.y, location.z],
        "rotation": [actor.get_actor_rotation().pitch, actor.get_actor_rotation().yaw, actor.get_actor_rotation().roll],
        "scale": [actor.get_actor_scale3d().x, actor.get_actor_scale3d().y, actor.get_actor_scale3d().z]
    }

    grid_data[grid_key]["actors"].append(actor_info)

# JSONファイルとして保存
for grid_key, data in grid_data.items():
    file_path = os.path.join(output_dir, f"grid_{grid_key}.json")
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

unreal.log(f"Exported grid data to {output_dir}")

