#shader vertex
#version 330 core

layout(location = 0) in vec4 position;

uniform mat4 uMVP;

void main()
{
  gl_Position = uMVP * position;
}

#shader fragment
#version 330 core

layout(location = 0) out vec4 color;
layout(location = 1) in vec3 vColor;

void main()
{
  color = vec4(vColor, 1.0);
}