import tensorflow as tf


class SessionManager:
    def __init__(self, sess, base_path='results/', checkpoint_freq=100):
        self.sess = sess
        self.saver = None
        self.base_path = base_path
        self.checkpoint_freq = checkpoint_freq
        self.global_step = tf.train.get_or_create_global_step()
        self.summary_writer = tf.summary.FileWriter(self.summaries_path)

    def restore_or_init(self):
        self.saver = tf.train.Saver()
        checkpoint = tf.train.latest_checkpoint(self.checkpoints_path)
        if checkpoint:
            self.saver.restore(self.sess, checkpoint)
        else:
            self.sess.run(tf.global_variables_initializer())

    def run(self, tf_op, tf_inputs, inputs):
        return self.sess.run(tf_op, feed_dict=dict(zip(tf_inputs, inputs)))

    def on_update(self, step):
        if step % self.checkpoint_freq:
            return
        self.saver.save(self.sess, self.checkpoints_path + '/ckpt', global_step=step)

    def add_summaries(self, tags, values, prefix='', step=None):
        for tag, value in zip(tags, values):
            self.add_summary(tag, value, prefix, step)

    def add_summary(self, tag, value, prefix='', step=None):
        summary = self.create_summary(prefix + '/' + tag, value)
        self.summary_writer.add_summary(summary, global_step=step)

    @staticmethod
    def create_summary(tag, value):
        return tf.Summary(value=[tf.Summary.Value(tag=tag, simple_value=value)])

    @property
    def start_step(self):
        return self.global_step.eval(session=self.sess)

    @property
    def summaries_path(self):
        return self.base_path + '/summaries'

    @property
    def checkpoints_path(self):
        return self.base_path + '/checkpoints'