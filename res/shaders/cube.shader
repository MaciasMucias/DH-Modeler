#shader vertex
#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

out vec3 FragPos;
out vec3 Normal;
out mat4 vView;

uniform mat4 uProjection;
uniform mat4 uView;
uniform mat4 uModel;

void main()
{

  FragPos = vec3(uModel * vec4(position, 1.0));
  Normal = mat3(transpose(inverse(uModel))) * normal;
  vView = uView;

  gl_Position = uProjection * uView * vec4(FragPos, 1.0);
}

#shader fragment
#version 330 core

layout(location = 0) out vec4 color;

in vec3 FragPos;
in vec3 Normal;
in mat4 vView;

uniform vec3 uColor;
vec3 lightColor = vec3(1.0, 1.0, 1.0);
vec4 lightPos = vec4(1.0, 1.0, 1.0, 1.0);
float ambientStrength = 0.7;

void main()
{

  vec3 norm = normalize(Normal);
  vec3 lightDir = normalize(vec3(vView * lightPos) - FragPos);
  float diff = max(dot(norm, lightDir), 0.0);

  vec3 ambient = ambientStrength * lightColor;
  vec3 diffuse = diff * lightColor;
  vec3 result = (ambient + diffuse) * uColor;
  color = vec4(result, 1.0);
}