import logging

from unitytrainers.trainer import UnityTrainerException

logger = logging.getLogger("unityagents")


class Policy(object):
    """
    Contains a TensorFlow model, and the necessary
    functions to interact with it to perform inference and updating
    """
    def __init__(self, seed, brain, trainer_parameters, sess):
        """
        Initialized the policy.
        :param seed: Random seed to use for TensorFlow.
        :param brain: The corresponding Brain for this policy.
        :param trainer_parameters: The trainer parameters.
        :param sess: The current TensorFlow session.
        """
        self.m_size = None
        self.model = None
        self.inference_dict = {}
        self.update_dict = {}
        self.sequence_length = 1
        self.seed = seed
        self.brain = brain
        self.variable_scope = trainer_parameters['graph_scope']
        self.use_recurrent = trainer_parameters["use_recurrent"]
        self.use_continuous_act = (brain.vector_action_space_type == "continuous")
        self.use_visual_obs = (brain.number_visual_observations > 0)
        self.use_vector_obs = (brain.vector_observation_space_size > 0)
        self.sess = sess
        if self.use_recurrent:
            self.m_size = trainer_parameters["memory_size"]
            self.sequence_length = trainer_parameters["sequence_length"]
            if self.m_size == 0:
                raise UnityTrainerException("The memory size for brain {0} is 0 even "
                                            "though the trainer uses recurrent."
                                            .format(brain.brain_name))
            elif self.m_size % 4 != 0:
                raise UnityTrainerException("The memory size for brain {0} is {1} "
                                            "but it must be divisible by 4."
                                            .format(brain.brain_name, self.m_size))

    def inference(self, brain_info):
        """
        Performs inference pass on model.
        :param brain_info: BrainInfo input to network.
        :return: Output from network based on self.inference_dict.
        """
        return None

    def update(self, batch, n_sequences, i):
        """
        Performs update on model.
        :param batch: Buffer of experiences.
        :param n_sequences: Number of sequences to process.
        :param i: Buffer index.
        :return: Results of update.
        """
        return None

    @property
    def graph_scope(self):
        """
        Returns the graph scope of the trainer.
        """
        return self.variable_scope

    def get_current_step(self):
        """
        Gets current model step.
        :return: current model step.
        """
        step = self.sess.run(self.model.global_step)
        return step

    def increment_step(self):
        """
        Increments model step.
        """
        self.sess.run(self.model.increment_step)

    def get_inference_vars(self):
        """
        :return:list of inference var names
        """
        return list(self.inference_dict.keys())

    def get_update_vars(self):
        """
        :return:list of update var names
        """
        return list(self.update_dict.keys())
