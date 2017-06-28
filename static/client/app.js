(function () {
    'use strict';
    
    angular
        .module('bepatientDeploy', []);


    angular
        .module('bepatientDeploy')
        .service('bepatientDeployService', bepatientDeployService);

    function bepatientDeployService($q, $http) {
        const apiURL = ''
        
        return {
            loadBranches: loadBranches,
            deployBranch: deployBranch,
            deleteBranch: deleteBranch
        }
        function deleteBranch(branch) {
            return $http({url: apiURL + '/' + branch,
                                  method: 'DELETE'});
        }
        function loadBranches() {
            return $http.get(apiURL + '/branch');
        }
        function deployBranch(branch) {
            return $http.post(apiURL + '/' + branch);
        }
    }

    angular
        .module('bepatientDeploy')
        .controller('bepatientDeployController', bepatientDeployController);

    function bepatientDeployController(bepatientDeployService) {
        var vm = this;        
        vm.name = "bepatientDeployController";
        vm.deployBranch = deployBranch;
        vm.deleteBranch = deleteBranch;

        /////
        
        function activate() {
            vm.message = "Loading...";
            bepatientDeployService
                .loadBranches()
                .then(function(request) {
                    vm.branches = request.data;
                    vm.message = "";
                })
                .catch(function(error) {
                    vm.message = "A server error occured while loading the branches"
                });
        }

        function deleteBranch(branch) {
            vm.message = "Deleting branch " + branch + "...";
            bepatientDeployService
                .deleteBranch(branch)
                .then(function(request) {
                    vm.message = "Branch deleted"
                })
                .catch(function(error) {
                    vm.message = "A server error occured, please check the name of the branch you are trying to clone";
                });
        }
        
        function deployBranch(branch) {
            vm.message = "Deploying branch... This may take up to a few minutes"
            
            bepatientDeployService
                .deployBranch(branch)
                .then(function (request) {
                    vm.message = ""
                    activate();
                })
                .catch (function (error) {
                    vm.message = "A server error occured, please check the name of the branch you are trying to clone";
                });
        }

        activate()
    }
    
})();
