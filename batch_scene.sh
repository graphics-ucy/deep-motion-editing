for d in ./example_data/*
do
	( ./blender -P blender_rendering/multi_bvh_import.py -- --dir_path "$d" )
done

