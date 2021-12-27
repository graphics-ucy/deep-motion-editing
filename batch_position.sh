
for i in `find ./example_data/ -name "*.blend" -type f`;
do
	( ./blender "$i" --background --python blender_rendering/positioning_figures.py )
done

