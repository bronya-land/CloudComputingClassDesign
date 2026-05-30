FROM nginx:1.25-alpine
# 将自定义 nginx 配置覆盖默认配置
COPY nginx.conf /etc/nginx/conf.d/default.conf
# 将前端静态文件复制到 Nginx 默认目录
COPY static/ /usr/share/nginx/html/
# 注意：static/index.html 中需包含学号和姓名，用于答辩识别
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]