FROM amazon/aws-cli

RUN yum update
RUN yum -y install python3
RUN yum -y install mesa-libGLU-devel.x86_64
RUN yum -y install libquadmath
RUN yum -y install fontconfig freetype freetype-devel fontconfig-devel libstdc++
RUN yum -y install tar

# COPY metashape-pro_1_8_3_amd64.tar.gz /metashape/metashape-pro_1_8_3_amd64.tar.gz
#
# RUN gunzip /metashape/metashape-pro_1_8_3_amd64.tar.gz
# RUN tar -xvf /metashape/metashape-pro_1_8_3_amd64.tar -C /metashape
# COPY metashape_aug2022.lic /metashape/metashape-pro/metashape_aug2022.lic
COPY src /metashape/src
COPY process.sh /metashape/process.shgit init
RUN chmod 777 /metashape/process.sh

ENTRYPOINT ["/metashape/process.sh"]
CMD ["match_photos"]
