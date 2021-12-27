
for i in `find ./example_data/ -name "*.blend" -type f`;
do
	( ./blender "$i" --background --python blender_rendering/color_figures.py )
done


