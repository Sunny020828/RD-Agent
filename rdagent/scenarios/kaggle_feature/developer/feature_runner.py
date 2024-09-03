from pathlib import Path

from rdagent.components.runner import CachedRunner
from rdagent.components.runner.conf import RUNNER_SETTINGS
from rdagent.core.exception import FactorEmptyError
from rdagent.scenarios.kaggle_feature.experiment.feature_experiment import KGFeatureExperiment


class KGFeatureRunner(CachedRunner[KGFeatureExperiment]):
    def develop(self, exp: KGFeatureExperiment) -> KGFeatureExperiment:
        # if RUNNER_SETTINGS.cache_result:
        #     cache_hit, result = self.get_cache_result(exp)
        #     if cache_hit:
        #         exp.result = result
        #         return exp

        #TODO 多个feat文件
        is_implemented = 0
        for i, feat in enumerate(exp.sub_workspace_list):
            feat_code = feat.code_dict.get("factor.py")
            if feat_code:
                is_implemented += 1
            else:
                continue
            renamed_feat_code = f"feat_{i}.py"
            exp.experiment_workspace.inject_code(**{renamed_feat_code: feat_code})
        if is_implemented == 0:
            raise FactorEmptyError("No factor is implemented")

        env_to_use = {"PYTHONPATH": "./"}

        result = exp.experiment_workspace.execute(run_env=env_to_use)

        exp.result = result
        # if RUNNER_SETTINGS.cache_result:
        #     self.dump_cache_result(exp, result)

        return exp
