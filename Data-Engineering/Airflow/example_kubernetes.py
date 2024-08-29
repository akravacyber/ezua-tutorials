#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
This is an example dag for using the KubernetesPodOperator.
"""
import logging

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

from kubernetes.client import models as k8s

log = logging.getLogger(__name__)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "max_active_runs": 1,
    "retries": 0,
}

dag = DAG(
    dag_id='example_kubernetes_operator',
    default_args=default_args,
    schedule_interval=None,
    tags=['example'],
    access_control={"All": {"can_read", "can_edit", "can_delete"}},
)

k = KubernetesPodOperator(
    dag=dag,
    namespace='mlflow',
    image="ubuntu:latest",
    cmds=["bash", "-cx"],
    arguments=["echo hello here"],
    name="airflow-test-pod",
    task_id="task",
    is_delete_operator_pod=False,
    volumes=[
        k8s.V1Volume(
            name="test-volume",
            persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name="mlflow-pvc"),
        ),
    ],
    volume_mounts=[
        k8s.V1VolumeMount(
            name="test-volume", mount_path="/mnt/test", read_only=True
        )
    ],
)
