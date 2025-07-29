#version 430

in uint space;
in vec3 v_position;
in vec3 v_normal;
in vec4 v_color;
in float v_layer;
in uint v_ident;
in uint v_flags;

uniform mat4 proj;
buffer b_spaces {
	mat4 spaces[];  // the GPU and CPU allocated buffers can be smaller, but we need to define a max size
};
uniform uint startident;

out vec3 normal;
out vec3 sight;
out vec4 color;
flat out uint identcolor;

vec3 sight_direction(vec4 p) {
	float f = proj[3][3] / dot(transpose(proj)[3], p) - 1;
	return vec3(p) * vec3(f,f,-1);
}

void main() 
{
	color = v_color;
	identcolor = startident + v_ident;
	vec4 position = spaces[space] * vec4(v_position,1);
	normal = mat3(spaces[space]) * v_normal;
	sight = sight_direction(position);
	gl_Position = proj * position;
	gl_Position[2] += v_layer * gl_Position[3];
}
