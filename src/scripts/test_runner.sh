#!/bin/sh

export new_image=$image/${GIT_BRANCH}:${GIT_COMMIT}
pod_name=$($kubectl get po -l app=platform-server-qa | awk 'NR>1 {print $1}')
echo "Pod name is: ${pod_name}"
echo "TEST_GROUP is: ${TEST_GROUP}"
echo "USE_TEST_GROUP: ${USE_TEST_GROUP}"
test_group_param=""
if [[ ! -z ${TEST_GROUP} ]]; then
	test_group_param="-m ${TEST_GROUP}"
fi

if [[ ${USE_TEST_GROUP} = true ]]; then
	$kubectl exec -it ${pod_name} -- python -m pytest -vv project/tests ${test_group_param} -rEf --maxfail=100 --alluredir=project/src/repository/allure_results
fi
