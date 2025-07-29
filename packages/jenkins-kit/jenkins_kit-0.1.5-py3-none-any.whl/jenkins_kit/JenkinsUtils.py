import jenkins
import chevron

class JenkinsUtils:
    def __init__(self, url, username, password):
        self.server = jenkins.Jenkins(url, username=username, password=password)
        self.existing_jobs = self.server.get_jobs()
        self.existing_job_names = [job['name'] for job in self.existing_jobs]

        self.build_job_template='''build(job: '{{job_name}}')'''
        self.stage_template='''
                        stage('Execute jobs in {{node_name}} Sequentially') {
                            steps {
                                {{{seq_builds}}}
                            }
                        }'''
        self.pipeline_template='''
        pipeline {
            agent none
            stages {
            {{{jobs_seq}}}
            }
        }'''
        self.parallel_template='''
                stage('Start jobs in nodes {{all_nodes}} Parallelly'){
                    parallel{
                        {{{multiple_stage}}}
                    }
                }'''

    def command_build(self,command):
        return f'''
    <hudson.tasks.BatchFile>
      <command>{command}</command>
      <configuredLocalRules/>
    </hudson.tasks.BatchFile>
'''

    def getJobTemplateXML(self,node,commands):
        commands=[self.command_build(i) for i in commands]
        commands_join="".join(commands)
        jobTemplateXML=f'''<?xml version='1.1' encoding='UTF-8'?>
<project>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty plugin="gitlab-plugin@1.5.33">
      <gitLabConnection></gitLabConnection>
      <jobCredentialId></jobCredentialId>
      <useAlternativeCredential>false</useAlternativeCredential>
    </com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty>
  </properties>
  <scm class="hudson.scm.NullSCM"/>
  <assignedNode>{node}</assignedNode>
  <canRoam>false</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>

  <builders>
    {commands_join}
  </builders>
  <publishers/>
  <buildWrappers/>
</project>
'''
        return jobTemplateXML

    def getPipleineTemplateXML(self,pipeline_script=''):
        pipelineTemplateXML=f'''<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job@1189.va_d37a_e9e4eda_">
  <actions>
    <org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobAction plugin="pipeline-model-definition@2.2114.v2654ca_721309"/>
    <org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction plugin="pipeline-model-definition@2.2114.v2654ca_721309">
      <jobProperties/>
      <triggers/>
      <parameters/>
      <options/>
    </org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction>
  </actions>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty plugin="gitlab-plugin@1.5.33">
      <gitLabConnection></gitLabConnection>
      <jobCredentialId></jobCredentialId>
      <useAlternativeCredential>false</useAlternativeCredential>
    </com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty>
  </properties>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2729.vea_17b_79ed57a_">
    <script>{pipeline_script}</script>
    <sandbox>true</sandbox>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>
'''
        return pipelineTemplateXML





    def get_existing_job_names(self):
        return self.existing_job_names

    def get_server(self):
        return self.server


    def create_pipeline_job(self,pipeline_jobname):
        if pipeline_jobname not in self.existing_job_names:
            print('Creating the Empty PipeLine Job:',pipeline_jobname)
            pipeline_xml=self.getPipleineTemplateXML(pipeline_script='')
            self.server.create_job(pipeline_jobname,pipeline_xml)
        else:
            print(f'{pipeline_jobname} already Exists!!')

    def reconfigure_pipeline(self,pipeline_jobname,dict_nodes_jobs):
        print('Reconfiguring the',pipeline_jobname)
        pipeline_xml=pipeline_xml.read()

        pipeline_script=self.create_pipeline(dict_nodes_jobs)
        pipeline_xml=self.getPipleineTemplateXML(pipeline_script=pipeline_script)
        self.server.reconfig_job(pipeline_jobname, pipeline_xml)

    def create_pipeline(self,dict_nodes_jobs):
        x=chevron.render(self.pipeline_template,{'jobs_seq':self.create_parallel_stages(dict_nodes_jobs)})
        return x

    def create_parallel_stages(self,dict_nodes_jobs):
        all_nodes=[node for node in dict_nodes_jobs]
        x=chevron.render(self.parallel_template,{'all_nodes':",".join(all_nodes), 'multiple_stage':self.create_stage(dict_nodes_jobs)})
        return x

    def create_stage(self,dict_nodes_jobs):
        stg=[]
        for node in dict_nodes_jobs:
            seq_jobs=dict_nodes_jobs[node]
            stg.append(chevron.render(self.stage_template,{'node_name':node,'seq_builds':self.build_job(seq_jobs)}))
        return "\n                ".join(stg)

    def build_job(self,seq_jobs):
        x=[]
        for seq_job in seq_jobs:
            x.append(chevron.render(self.build_job_template,{'job_name':seq_job}))
        return "\n                        ".join(x)