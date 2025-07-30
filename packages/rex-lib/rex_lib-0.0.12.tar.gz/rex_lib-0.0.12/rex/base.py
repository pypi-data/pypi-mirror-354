import functools
from typing import Any, Callable, Dict, List, Sequence, Tuple, TYPE_CHECKING, Union

import distrax
import equinox as eqx
import jax
import numpy as onp
from flax import struct
from flax.core import FrozenDict
from jax import numpy as jnp
from jax.typing import ArrayLike
from numpy import ma as ma

import rex.constants as constants
import rex.jax_utils as rjax


if TYPE_CHECKING:
    from rex.node import BaseNode


@struct.dataclass
class Base:
    """
    Base functionality extending all dataclasses.
    These methods allow for dataclasses to be operated like arrays/matrices.

    *Note*: Credits to the authors of the brax library for this implementation.

    Tip:
        Use this base class for all state, output, and param pytrees.
    """

    def __repr__(self):  # todo: this is not inherited by subclasses...
        return eqx.tree_pformat(self, short_arrays=False)

    def __str__(self):
        """Return a string representation of the dataclass."""
        return eqx.tree_pformat(self, short_arrays=False)

    def __add__(self, o: Any) -> Any:
        """
        Element-wise addition of two pytrees.

        Args:
            o: The other pytree to add.

        Returns:
            The resulting pytree after applying the element-wise operation.
        """
        try:
            # If o is a pytree, element-wise addition
            return jax.tree_util.tree_map(lambda x, y: x + y, self, o)
        except ValueError:
            # If o is a scalar, element-wise addition
            return jax.tree_util.tree_map(lambda x: x + o, self)

    def __sub__(self, o: Any) -> Any:
        """
        Element-wise subtraction of two pytrees.

        Args:
            o: The other pytree to add.

        Returns:
            The resulting pytree after applying the element-wise operation.
        """
        try:
            # If o is a pytree, element-wise subtraction
            return jax.tree_util.tree_map(lambda x, y: x - y, self, o)
        except ValueError:
            # If o is a scalar, element-wise subtraction
            return jax.tree_util.tree_map(lambda x: x - o, self)

    def __mul__(self, o: Any) -> Any:
        """
        Element-wise multiplication of two pytrees.

        Args:
            o: The other pytree to add.

        Returns:
            The resulting pytree after applying the element-wise operation.
        """
        try:
            # If o is a pytree, element-wise multiplication
            return jax.tree_util.tree_map(lambda x, y: x * y, self, o)
        except ValueError:
            # If o is a scalar, element-wise multiplication
            return jax.tree_util.tree_map(lambda x: x * o, self)

    def __neg__(self) -> Any:
        """
        Element-wise negation of two pytrees.

        Returns:
            The resulting pytree after applying the element-wise operation.
        """
        return jax.tree_util.tree_map(lambda x: -x, self)

    def __truediv__(self, o: Any) -> Any:
        """
        Element-wise division of two pytrees.

        Args:
            o: The other pytree to add.

        Returns:
            The resulting pytree after applying the element-wise operation.
        """
        try:
            # If o is a pytree, element-wise division
            return jax.tree_util.tree_map(lambda x, y: x / y, self, o)
        except ValueError:
            # If o is a scalar, element-wise division
            return jax.tree_util.tree_map(lambda x: x / o, self)

    def __getitem__(self, val: int) -> Any:
        """Get a specific value from the dataclass.

        Args:
            val: The value to get from the dataclass.

        Returns:
            The value from the dataclass.
        """
        return jax.tree_util.tree_map(lambda x: x[val], self)

    def replace(self, *args: Any, **kwargs: Any) -> Any:
        """Replace fields in the dataclass.

        Args:
            *args: The fields to replace.
            **kwargs: The fields to replace.
        """
        return self.replace(*args, **kwargs)

    def reshape(self, shape: Sequence[int]) -> Any:
        """
        Reshape the dataclass.

        Args:
            shape: The shape to reshape the dataclass.

        Returns:
            The reshaped dataclass.
        """
        return jax.tree_util.tree_map(lambda x: x.reshape(shape), self)

    def select(self, o: Any, cond: jax.Array) -> Any:
        """
        Select elements from two pytrees based on a condition

        Args:
            o: The other pytree to select elements from.
            cond: The condition to select elements based on.

        Returns:
            The resulting pytree after applying the condition
        """
        return jax.tree_util.tree_map(lambda x, y: (x.T * cond + y.T * (1 - cond)).T, self, o)

    def slice(self, beg: int, end: int) -> Any:
        """
        Slice the dataclass.

        Args:
            beg: The beginning of the slice.
            end: The end of the slice.

        Returns:
            The sliced dataclass.
        """
        return jax.tree_util.tree_map(lambda x: x[beg:end], self)

    def take(self, i: int, axis: int = 0) -> Any:
        """
        Take elements from the dataclass.

        Args:
            i: The elements to take.
            axis: The axis to take the elements from.

        Returns:
            The taken elements from the dataclass.
        """
        return jax.tree_util.tree_map(lambda x: jnp.take(x, i, axis=axis, mode="wrap"), self)

    def concatenate(self, *others: Any, axis: int = 0) -> Any:
        """
        Concatenate the dataclass with other dataclasses.

        Args:
            *others: The other dataclasses to concatenate.
            axis: The axis to concatenate the dataclasses on.

        Returns:
            The concatenated dataclass
        """
        return jax.tree_util.tree_map(lambda *x: jnp.concatenate(x, axis=axis), self, *others)

    def index_set(self, idx: Union[jax.Array, Sequence[jax.Array]], o: Any) -> Any:
        """
        Set elements in the dataclass based on an index.

        Args:
            idx: The index to set the elements.
            o: The elements to set.

        Returns:
            The dataclass with the elements
        """
        return jax.tree_util.tree_map(lambda x, y: x.at[idx].set(y), self, o)

    def index_sum(self, idx: Union[jax.Array, Sequence[jax.Array]], o: Any) -> Any:
        """
        Sum elements in the dataclass based on an index.

        Args:
            idx: The index to sum the elements.
            o: The elements to sum.

        Returns:
            The dataclass with the summed elements.
        """
        return jax.tree_util.tree_map(lambda x, y: x.at[idx].add(y), self, o)


@struct.dataclass
class Empty(Base):
    """Empty class."""

    pass


PyTree = Any
Output = Union[PyTree, Base]
State = Union[PyTree, Base]
Params = Union[PyTree, Base]
GraphBuffer = FrozenDict[str, Output]


@struct.dataclass
class Edge:
    """And edge data structure that holds the sequence numbers and timestamps of a connection.

    This data structure may be batched and hold data for multiple episodes.
    The last dimension represent the data during the episode.

    Given a message from  node_out to node_in, the sequence number of the send message is seq_out. The message is received
    at node_in at time ts_recv. Seq_in is the sequence number of the call that node_in processes the message.

    When there are outputs that were never received, set the seq_in to -1.

    In case the received timestamps are not available, set ts_recv to a dummy value (e.g. 0.0).

    Attributes:
        seq_out: The sequence number of the message. Must be monotonically increasing.
        seq_in: The sequence number of the call that the message is processed. Must be monotonically increasing.
        ts_recv: The time the message is received at the input node. Must be monotonically increasing.
    """

    seq_out: Union[int, jax.Array]
    seq_in: Union[int, jax.Array]
    ts_recv: Union[float, jax.Array]


@struct.dataclass
class Vertex:
    """A vertex data structure that holds the sequence numbers and timestamps of a node.

    This data structure may be batched and hold data for multiple episodes.
    The last dimension represent the sequence numbers during the episode.

    In case the timestamps are not available, set ts_start and ts_end to a dummy value (e.g. 0.0).

    Ideally, for every vertex seq[i] there should be an edge with seq_out[i] for every connected node in the graph.

    Attributes:
        seq: The sequence number of the node. Should start at 0 and increase by 1 every step (no gaps).
        ts_start: The start time of the computation of the node (i.e. when the node starts processing step 'seq').
        ts_end: The end time of the computation of the node (i.e. when the node finishes processing step 'seq').
    """

    seq: Union[int, jax.Array]
    ts_start: Union[float, jax.Array]
    ts_end: Union[float, jax.Array]


@struct.dataclass
class Graph:
    """A computation graph data structure that holds the vertices and edges of a computation graph.

    This data structure is used to represent the computation graph of a system. It holds the vertices and edges of the
    graph. The vertices represent consecutive step calls of nodes, and the edges represent the data flow between connected
    nodes.

    Stateful edges must not be included in the edges, but are implicitly assumed. In other words, consecutive sequence numbers
    of the same node are assumed to be connected.

    The graph should be directed and acyclic. Cycles are not allowed.

    Attributes:
        vertices: A dictionary of vertices. The keys are the unique names of the node type, and the values are the vertices.
        edges: A dictionary of edges. The keys are of the form (n1, n2), where n1 and n2 are the unique names of the
               output and input nodes, respectively. The values are the edges.
    """

    vertices: Dict[str, Vertex]
    edges: Dict[Tuple[str, str], Edge]

    def __len__(self) -> int:
        """
        Get the number of episodes in the graph.

        Returns:
            The number of episodes (i.e. the number of graphs if the graph is batched).
        """
        shape = next(iter(self.vertices.values())).seq.shape
        if len(shape) > 1:
            return shape[0]
        else:
            return 1

    def __getitem__(self, val: int) -> "Graph":
        """
        In case the graph is batched, and holds the graphs of multiple episodes,
        this function returns the graph of a specific episode.

        Args:
            val: The episode to get the graph of.

        Returns:
            The graph of the specific episode.
        """
        shape = next(iter(self.vertices.values())).seq.shape
        if len(shape) == 0:
            raise ValueError("Graph is not batched.")
        else:
            return jax.tree_util.tree_map(lambda v: v[val], self)

    @staticmethod
    def stack(graphs_raw: List["Graph"]) -> "Graph":
        """
        Stack multiple graphs into a single graph.

        Note: Padding
            If the graphs have different lengths, the vertices and edges are padded with -1.

        Args:
            graphs_raw: A list of graphs to stack.

        Returns:
            A single graph with the vertices and edges stacked
        """
        # Note: Vertex.seq=-1, .ts_start=-1., .ts_end=-1. for padded vertices
        # Note: Edge.seq_out=-1, .seq_in=-1., .ts_recv=-1. for padded edges or edges that were never received.
        # Convert to graphs

        def _stack(*_graphs):
            """Stack the vertices and edges of the graphs."""
            _max_len = max(len(arr) for arr in _graphs)
            # Pad with -1
            _padded = tuple(onp.pad(arr, (0, _max_len - len(arr)), constant_values=-1) for arr in _graphs)
            return onp.stack(_padded, axis=0)

        graphs = jax.tree_util.tree_map(_stack, *graphs_raw)
        return graphs

    def filter(self, nodes: Dict[str, "BaseNode"], filter_edges: bool = True) -> "Graph":
        """Filter the graph to only include the nodes and edges that are in the nodes dictionary.

        Args:
            nodes: A dictionary of nodes. The keys are the unique names of the nodes, and the values are the nodes.
            filter_edges:  If True, only include the nodes that are connected to the nodes in the dictionary.

        Returns:
            A new graph with only the nodes and edges that are in the nodes dictionary.
        """
        # Determine set of vertices and connections to keep
        connections = set()
        for n2, v2 in nodes.items():
            if filter_edges:  # Also filter edges that only exist between vertices in `nodes`
                for n1, i in v2.inputs.items():
                    if n1 in nodes:
                        connections.add((n1, n2))
            else:  # Only filters vertices, meaning vertices may have more edges than connections in nodes.
                if n2 in self.vertices:
                    for n1, _ in filter(lambda x: x[1] == n2, self.edges):
                        if n1 in nodes:
                            connections.add((n1, n2))

        # Perform filtering of vertices and edges
        vertices = self.vertices.copy()
        edges = self.edges.copy()
        v_names = list(vertices.keys())
        e_names = list(edges.keys())
        for k in v_names:
            if k not in nodes:
                vertices.pop(k)
        for n1, n2 in e_names:
            if (n1, n2) not in connections:
                edges.pop((n1, n2))
        return Graph(vertices=vertices, edges=edges)


@struct.dataclass
class Window:
    """A window buffer that holds the sequence numbers and timestamps of a connection.

    Internal use only.
    """

    seq: Union[int, jax.Array]  # seq_out
    ts_sent: Union[float, jax.Array]  # ts_end[seq_out]
    ts_recv: Union[float, jax.Array]

    def __getitem__(self, val):
        return jax.tree_util.tree_map(lambda v: v[val], self)

    def _shift(self, a: jax.typing.ArrayLike, new: jax.typing.ArrayLike):
        rolled_a = jnp.roll(a, -1, axis=0)
        new_a = jnp.array(rolled_a).at[-1].set(jnp.array(new))
        return new_a

    def push(self, seq, ts_sent, ts_recv) -> "Window":
        seq = self._shift(self.seq, seq)
        ts_sent = self._shift(self.ts_sent, ts_sent)
        ts_recv = self._shift(self.ts_recv, ts_recv)
        return Window(seq=seq, ts_sent=ts_sent, ts_recv=ts_recv)


@struct.dataclass
class WindowedVertex(Vertex):
    """A vertex with windows.

    Internal use only.
    """

    windows: Dict[str, Window]


@struct.dataclass
class WindowedGraph:
    """A graph with windows.

    Internal use only.
    """

    vertices: Dict[str, WindowedVertex]

    def __getitem__(self, val):
        return jax.tree_util.tree_map(lambda v: v[val], self)

    def to_graph(self) -> Graph:
        num_graphs = next(iter(self.vertices.values())).seq.shape[0]
        vertices = {n: Vertex(seq=v.seq, ts_start=v.ts_start, ts_end=v.ts_end) for n, v in self.vertices.items()}
        edges = dict()
        for n2, v2 in self.vertices.items():
            for n1, w in v2.windows.items():
                # Repeat seq_in to match the shape of seq_out
                seq_in = jnp.repeat(v2.seq, w.seq.shape[-1], axis=-1).reshape(num_graphs, -1, w.seq.shape[-1])

                # Flatten
                seq_out = w.seq.reshape(num_graphs, -1)
                seq_in = seq_in.reshape(num_graphs, -1)
                ts_recv = w.ts_recv.reshape(num_graphs, -1)
                edges[(n1, n2)] = Edge(seq_out=seq_out, seq_in=seq_in, ts_recv=ts_recv)
        return Graph(vertices=vertices, edges=edges)


@struct.dataclass
class SlotVertex(WindowedVertex):
    """A vertex with slots.

    Internal use only.
    """

    run: Union[bool, jax.Array]
    kind: str = struct.field(pytree_node=False)
    generation: int = struct.field(pytree_node=False)


@struct.dataclass
class Timings:
    """A data structure that holds the timings of the execution of a graph.

    Can be retrieved from the graph with graph.timings.

    Internal use only.
    """

    slots: Dict[str, SlotVertex]

    def to_generation(self) -> List[Dict[str, SlotVertex]]:
        generations = {}
        for n, s in self.slots.items():
            if s.generation not in generations:
                generations[s.generation] = {}
            generations[s.generation][n] = s
        return [generations[i] for i in range(len(generations))]

    def get_masked_timings(self):
        np_timings = jax.tree_util.tree_map(lambda v: onp.array(v), self)

        # Get node names
        node_kinds = set([s.kind for key, s in np_timings.slots.items()])

        # Convert timings to list of generations
        timings = {}
        for n, v in np_timings.slots.items():
            if v.generation not in timings:
                timings[v.generation] = {}
            timings[v.generation][n] = v
        timings = [timings[i] for i in range(len(timings))]

        # Get output buffer sizes
        masked_timings_slot = []
        for i_gen, gen in enumerate(timings):
            # t_flat = {slot: t for slot, t in gen.items()}
            slots = {k: [] for k in node_kinds}
            [slots[v.kind].append(v) for k, v in gen.items()]
            [slots.pop(k) for k in list(slots.keys()) if len(slots[k]) == 0]
            # slots:= [eps, step, slot_idx, window=optional]
            slots = {k: jax.tree_util.tree_map(lambda *args: onp.stack(args, axis=2), *v) for k, v in slots.items()}

            def _mask(mask, arr):
                # Repeat mask in extra dimensions of arr (for inputs)
                if arr.ndim > mask.ndim:
                    extra_dim = tuple([mask.ndim + a for a in range(arr.ndim - mask.ndim)])
                    new_mask = onp.expand_dims(mask, axis=extra_dim)
                    for i in extra_dim:
                        new_mask = onp.repeat(new_mask, arr.shape[i], axis=-1)
                else:
                    new_mask = mask
                # print(mask.shape, arr.shape, new_mask.shape)
                masked_arr = ma.masked_array(arr, mask=new_mask)
                return masked_arr

            masked_slots = {k: jax.tree_util.tree_map(functools.partial(_mask, ~v.run), v) for k, v in slots.items()}
            masked_timings_slot.append(masked_slots)

        def _update_mask(j, arr):
            arr.mask[:, :, :, j] = True
            return arr

        def _concat_arr(a, b):
            return ma.concatenate((a, b), axis=2)

        # Combine timings for each slot. masked_timings := [eps, step, slot_idx, gen_idx, window=optional]
        masked_timings = {}
        for i_gen, gen in enumerate(masked_timings_slot):
            for key, t in gen.items():
                # Repeat mask in extra dimensions of arr (for number of gens, and mask all but the current i_gen)
                t = jax.tree_util.tree_map(lambda x: onp.repeat(x[:, :, :, None], len(timings), axis=3), t)

                # Update mask to be True for all other gens
                for j in range(len(timings)):
                    if j == i_gen:
                        continue
                    jax.tree_util.tree_map(functools.partial(_update_mask, j), t)

                # Add to masked_timings
                if key not in masked_timings:
                    # Add as new entry
                    masked_timings[key] = t.replace(generation=None)
                else:
                    # Concatenate with existing entry
                    t = t.replace(generation=masked_timings[key].generation)  # Ensures that static fields are the same
                    masked_timings[key] = jax.tree_util.tree_map(_concat_arr, masked_timings[key], t)
        return masked_timings

    def get_buffer_sizes(self):
        # Get masked timings:= [eps, step, slot_idx, gen_idx, window=optional]
        masked_timings = self.get_masked_timings()

        # Get min buffer size for each node
        name_mapping = {n: {o: o for o in s.windows} for n, s in masked_timings.items()}
        min_buffer_sizes = {
            k: {input_name: output_name for input_name, output_name in inputs.items()} for k, inputs in name_mapping.items()
        }
        node_buffer_sizes = {n: [] for n in masked_timings.keys()}
        for n, inputs in name_mapping.items():
            t = masked_timings[n]
            # t.windows["pid"].seq[0, -1, :, :, :]
            for input_name, output_name in inputs.items():
                # Determine min input sequence per generation (i.e. we reduce over all slots within a generation & window)
                seq_in = onp.amin(t.windows[input_name].seq, axis=(2, 4))
                seq_in = seq_in.reshape(
                    *seq_in.shape[:-2], -1
                )  # flatten over generation & step dimension (i.e. [s1g1, s1g2, ..], [s2g1, s2g2, ..], ..)
                # NOTE: fill masked steps with max value (to not influence buffer size)
                ma.set_fill_value(
                    seq_in, onp.iinfo(onp.int32).max
                )  # Fill with max value, because it will not influence the min
                filled_seq_in = seq_in.filled()
                max_seq_in = onp.minimum.accumulate(filled_seq_in[:, ::-1], axis=-1)[:, ::-1]

                # Determine max output sequence per generation
                seq_out = onp.amax(
                    masked_timings[output_name].seq, axis=(2,)
                )  # (i.e. we reduce over all slots within a generation)
                seq_out = seq_out.reshape(
                    *seq_out.shape[:-2], -1
                )  # flatten over generation & step dimension (i.e. [s1g1, s1g2, ..], [s2g1, s2g2, ..], ..)
                ma.set_fill_value(
                    seq_out, onp.iinfo(onp.int32).min
                )  # todo: CHECK! changed from -1 to onp.iinfo(onp.int32).min to deal with negative seq numbers
                filled_seq_out = seq_out.filled()
                max_seq_out = onp.maximum.accumulate(filled_seq_out, axis=-1)

                # Calculate difference to determine buffer size
                # NOTE: Offset output sequence by +1, because the output is written to the buffer AFTER the buffer is read
                offset_max_seq_out = onp.roll(max_seq_out, shift=1, axis=1)
                offset_max_seq_out[:, 0] = onp.iinfo(
                    onp.int32
                ).min  # todo: CHANGED to min value compared to --> NOTE: First step is always -1, because no node has run at this point.
                s = offset_max_seq_out - max_seq_in

                # NOTE! +1, because, for example, when offset_max_seq_out = 0, and max_seq_in = 0, we need to buffer 1 step.
                max_s = s.max() + 1

                # Store min buffer size
                min_buffer_sizes[n][input_name] = max_s
                node_buffer_sizes[output_name].append(max_s)

        return node_buffer_sizes

    def get_output_buffer(
        self, nodes: Dict[str, "BaseNode"], sizes=None, extra_padding: int = 0, graph_state=None, rng: jax.Array = None
    ):
        if rng is None:
            rng = jax.random.PRNGKey(0)
        # if graph_state is None:
        #     raise ValueError("graph_state is required to get the output buffer.")

        # Get buffer sizes if not provided
        if sizes is None:
            sizes = self.get_buffer_sizes()

        # Create output buffers
        buffers = {}
        stack_fn = lambda *x: jnp.stack(x, axis=0)
        rngs = jax.random.split(rng, num=len(nodes))
        for idx, (n, s) in enumerate(sizes.items()):
            assert n in nodes, f"Node `{n}` not found in nodes."
            buffer_size = max(s) + extra_padding if len(s) > 0 else max(1, extra_padding)
            assert buffer_size > 0, f"Buffer size for node `{n}` is 0."
            b = jax.tree_util.tree_map(stack_fn, *[nodes[n].init_output(rngs[idx], graph_state=graph_state)] * buffer_size)
            buffers[n] = b
        return FrozenDict(buffers)


@struct.dataclass
class DelayDistribution:
    """A delay distribution data structure."""

    def reset(self, rng: jax.Array) -> "DelayDistribution":
        """
        Reset the distribution (e.g. random number generator).

        Args:
            rng: random number generator

        Returns:
            DelayDistribution: the reset distribution
        """
        raise NotImplementedError("DelayDistribution.reset is not implemented.")

    @staticmethod
    def sample_pure(delay_dist: "DelayDistribution", shape: Union[int, Tuple] = None) -> Tuple["DelayDistribution", jax.Array]:
        return delay_dist.sample(shape)

    def sample(self, shape: Union[int, Tuple] = None) -> Tuple["DelayDistribution", jax.Array]:
        """
        Sample from the distribution.

        Args:
            shape: the shape of the sample

        Returns:
            The new distribution and the sample
        """
        raise NotImplementedError("DelayDistribution.sample is not implemented.")

    @staticmethod
    def quantile_pure(delay_dist: "DelayDistribution", q: float) -> float:
        return delay_dist.quantile(q)

    def quantile(self, q: float) -> float:
        """
        Compute the quantile of the distribution.

        Args:
            q: the quantile value

        Returns:
            The quantile value
        """
        raise NotImplementedError("DelayDistribution.quantile is not implemented.")

    @staticmethod
    def mean_pure(delay_dist: "DelayDistribution") -> float:
        return delay_dist.mean()

    def mean(self) -> float:
        """
        Compute the mean of the distribution.

        Returns:
            The mean value
        """
        raise NotImplementedError("DelayDistribution.mean is not implemented.")

    @staticmethod
    def pdf_pure(delay_dist: "DelayDistribution", x: float) -> float:
        return delay_dist.pdf(x)

    def pdf(self, x: float) -> float:
        """
        Compute the probability density function of the distribution.

        Args:
            x: the value at which to compute the pdf

        Returns:
            The pdf value
        """
        raise NotImplementedError("DelayDistribution.pdf is not implemented.")

    def window(self, rate_out) -> int:
        return 0

    def equivalent(self, other: "DelayDistribution") -> bool:
        return True

    def apply_delay(self, rate_out: float, input: "InputState", ts_start: Union[float, jax.typing.ArrayLike]) -> "InputState":
        return input


@struct.dataclass
class StaticDist(DelayDistribution):
    """
    A wrapper around distrax distributions to make them compatible with the DelayDistribution interface.

    Attributes:
        rng: the random number generator
        dist: the (static) distrax distribution (e.g. Normal, MixtureSameFamily, etc.)
    """

    rng: jax.Array
    dist: distrax.Distribution = struct.field(pytree_node=False)

    def reset(self, rng: jax.Array) -> "StaticDist":
        """
        Reset the random number generator.

        Args:
            rng: random number generator

        Returns:
            DelayDistribution: the reset distribution
        """
        return self.replace(rng=rng)

    @classmethod
    def create(cls, dist: distrax.Distribution) -> "StaticDist":
        """
        Create a static distribution.

        Args:
            dist: the distrax distribution

        Returns:
            The static distribution
        """
        return cls(rng=jax.random.PRNGKey(0), dist=dist)

    def sample(self, shape: Union[int, Tuple] = None) -> Tuple["StaticDist", jax.Array]:
        """
        Sample from the distribution.

        Args:
            shape: the shape of the sample

        Returns:
            The new distribution and the sample
        """
        if shape is None:
            shape = ()
        new_rng, rng_sample = jax.random.split(self.rng, 2)
        samples = self.dist.sample(sample_shape=shape, seed=rng_sample)
        samples = jnp.clip(samples, 0.0, None)  # Ensure that the delay is non-negative
        return self.replace(rng=new_rng), samples

    def quantile(self, q: float) -> Union[float, jax.typing.ArrayLike]:
        """
        Compute the quantile of the distribution.

        Args:
            q: the quantile value

        Returns:
            The quantile value
        """
        shape = q.shape if isinstance(q, (jax.Array, onp.ndarray)) else ()
        if isinstance(self.dist, distrax.Deterministic):
            res = onp.ones(shape) * self.dist.mean()
            return res
        elif isinstance(self.dist, distrax.Normal):
            # raise NotImplementedError("Quantile not tested for Normal distribution.")
            return jax.scipy.special.ndtri(q) * self.dist.scale + self.dist.loc
        elif isinstance(self.dist, distrax.MixtureSameFamily):
            import rex.utils as utils  # Avoid circular import

            cdist = self.dist.components_distribution
            qs_component_max = jax.scipy.special.ndtri(0.999) * cdist.scale + cdist.loc
            qs_component_min = jax.scipy.special.ndtri(0.001) * cdist.scale + cdist.loc
            qs = utils.mixture_distribution_quantiles(
                dist=self.dist,
                probs=jnp.array(q).reshape(-1),
                N_grid_points=int(1e3),
                grid_min=float(qs_component_min.min()) * 0.9,
                grid_max=float(qs_component_max.max()) * 1.1,
            )[0]
            return qs.reshape(shape)
        else:
            raise NotImplementedError(f"Quantile not implemented for distribution {self.dist}.")

    def mean(self) -> float:
        """
        Compute the mean of the distribution.

        Returns:
            The mean value
        """
        try:
            return self.dist.mean()
        except NotImplementedError as e:
            raise e

    def pdf(self, x: float) -> float:
        """
        Compute the probability density function of the distribution.

        Args:
            x: the value at which to compute the pdf

        Returns:
            The pdf value
        """
        return self.dist.prob(x)


@struct.dataclass
class TrainableDist(DelayDistribution):
    """
    Attributes:
        alpha: the value between [0, 1]
        min: the minimum expected delay
        max: the maximum expected delay
        interp: the interpolation method ("zoh", "linear", "linear_real_only").
                "zoh": zero-order hold interpolation between received messages.
                "linear": linear interpolation between received messages.
                "linear_real_only": Only start interpolating between received messages.
    """

    alpha: Union[float, jax.typing.ArrayLike] = struct.field(default=0.5)  # Value between [0, 1]
    min: Union[float, jax.typing.ArrayLike] = struct.field(pytree_node=False, default=0.0)  # Minimum expected delay
    max: Union[float, jax.typing.ArrayLike] = struct.field(pytree_node=False, default=0.0)  # Maximum expected delay
    interp: str = struct.field(pytree_node=False, default="zoh")  # "zoh", "linear", "linear_real_only"

    def reset(self, rng: jax.Array) -> "TrainableDist":
        """
        Does nothing as the distribution is deterministic.

        Args:
            rng: random number generator

        Returns:
            DelayDistribution: the reset distribution
        """
        # Not using the rng for now
        return self

    @classmethod
    def create(
        cls,
        delay: Union[float, jax.typing.ArrayLike],
        min: Union[float, jax.typing.ArrayLike],
        max: Union[float, jax.typing.ArrayLike],
        interp: str = "zoh",
    ) -> "TrainableDist":
        """
        Creates a trainable distribution.
        Converts the delay to alpha, which is the value between [0, 1].

        Args:
            delay: the desired delay
            min: the minimum expected delay
            max: the maximum expected delay
            interp: the interpolation method ("zoh", "linear", "linear_real_only").
        Returns:
            The trainable distribution
        """
        min = float(min)
        max = float(max)
        assert min < max, f"min should be less than max, but got min={min} and max={max}."
        alpha = float(TrainableDist._get_alpha(delay, min, max))
        assert 0.0 <= alpha <= 1.0, f"alpha should be between [0, 1], but got {alpha}."
        assert 0.0 <= min, f"min should be greater than or equal to 0, but got {min}."
        assert interp in ["zoh", "linear", "linear_real_only"], f"Interpolation method {interp} not supported."
        return cls(alpha=alpha, min=min, max=max, interp=interp)

    def sample(self, shape: Union[int, Tuple] = None) -> Tuple["TrainableDist", jax.Array]:
        """
        Sample from the distribution.

        Args:
            shape: the shape of the sample

        Returns:
            The new distribution and the sample
        """
        if shape is None:
            shape = ()
        # Sample and broadcast to shape size
        samples = self.min + self.alpha * (self.max - self.min) * jnp.ones(shape)
        return self, samples

    def quantile(self, q: float) -> float:
        """
        Compute the quantile of the distribution.

        As the distribution is deterministic, the quantile is trivially calculated as the
        constant value of the distribution.

        Args:
            q: the quantile value

        Returns:
            The quantile value
        """
        return self.min + self.alpha * (self.max - self.min)

    def mean(self) -> Union[float, jax.typing.ArrayLike]:
        """
        Compute the mean of the distribution.

        Returns:
            The mean value
        """
        return self.min + self.alpha * (self.max - self.min)

    def pdf(self, x: float) -> Union[jax.Array, float]:
        """
        Compute the probability density function of the distribution.

        Args:
            x: the value at which to compute the pdf

        Returns:
            The pdf value
        """
        mean = self.mean()
        return jnp.where(mean == x, 1.0, 0.0)

    def window(self, rate_out: Union[float, int]) -> int:
        """Compute the additional window size needed for the delay distribution.

        Args:
            rate_out: the output rate of the connection

        Returns:
            The additional window size needed for the delay distribution
        """
        return int(onp.ceil(rate_out * (self.max - self.min)).astype(int))

    def equivalent(self, other: "DelayDistribution") -> bool:
        """Check if two delay distributions are equivalent

        Args:
            other: the other delay distribution

        Returns:
            True if the two delay distributions are equivalent, False otherwise
        """
        if not isinstance(other, TrainableDist):
            return False  # Not the same distribution
        if self.max != other.max:
            return False  # Different max delay --> affects the window size & computation graph at compile time
        if self.min != other.min:
            return False  # Different min delay --> affects the window size & computation graph at compile time
        if self.interp != other.interp:  # Different interpolation method --> affects the computation graph at compile time
            return False
        return True

    def apply_delay(self, rate_out: float, input: "InputState", ts_start: Union[float, jax.typing.ArrayLike]) -> "InputState":
        """Apply the delay to the input state.

        The delay is determined by the delay distribution of the connection.

        Args:
            rate_out: the output rate of the connection
            input: the input state
            ts_start: the start time of the computation

        Returns:
            The input state with the delay applied. This reduces the window size of the input by self.window(rate_out).
        """
        # If no window, return the same input state
        window_delayed = self.window(rate_out)
        if window_delayed == 0:  # Return the input state if the only possible shift is 0.
            return input  # NOOP
        cum_window = input.seq.shape[0]
        window = cum_window - window_delayed
        new_delay_dist, d = self.sample()
        ts_recv = input.ts_sent + d
        ts_recv = jnp.where(input.seq < 0, input.ts_recv, ts_recv)  # If seq < 0, then keep the original ts_recv
        idx_max = jnp.argwhere(ts_recv > ts_start, size=1, fill_value=cum_window)[0, 0]
        if self.interp == "zoh":
            # Slice the input state
            idx_min = idx_max - window
            tb = [input.seq, input.ts_sent, ts_recv, input.data]
            slice_sizes = jax.tree_util.tree_map(lambda _tb: list(_tb.shape[1:]), tb)
            tb_delayed = jax.tree_util.tree_map(
                lambda _tb, _size: jax.lax.dynamic_slice(_tb, [idx_min] + [0 * s for s in _size], [window] + _size),
                tb,
                slice_sizes,
            )
            delayed_input_state = InputState(*tb_delayed, delay_dist=new_delay_dist)
        elif self.interp in ["linear", "linear_real_only"]:
            idx_min = idx_max - window
            if self.interp == "linear_real_only":
                # here, we only start interpolating between received messages (seq=>0).
                # That is, in case of seq=-1, we take the message with seq=-1.
                ts_recv_mask = jnp.where(input.seq < 0, -1e9, ts_recv)
            else:  # linear
                # Here, we also interpolate between real (seq=>0) and dummy messages (seq=-1).
                ts_recv_mask = ts_recv

            tb = [input.seq, input.ts_sent, ts_recv, input.data]
            ts_recv_interp = jax.lax.dynamic_slice(ts_recv_mask, [idx_min], [window])
            ts_recv_interp = ts_recv_interp + (ts_start - ts_recv_interp[-1])

            def interp_maybe_batched(_fp):
                if _fp.ndim > 1:
                    _fp_shape = _fp.shape
                    _fp_batch = _fp.reshape(_fp_shape[0], -1)  # Flatten all but the first dimension
                    _f_shape = (window,) + _fp_shape[1:]  # This is the shape of the output
                    res = jax.vmap(
                        jnp.interp,
                        in_axes=(
                            None,
                            None,
                            1,
                        ),
                    )(ts_recv_interp, ts_recv_mask, _fp_batch).reshape(_f_shape)
                else:
                    res = jnp.interp(ts_recv_interp, ts_recv_mask, _fp)
                return res.astype(
                    jax.dtypes.canonicalize_dtype(_fp.dtype)
                )  # Ensure that the dtype is the same as the original dtype

            # Now, ts_start == ts_recv_interp[-1] should hold.
            interp_tb = jax.tree_util.tree_map(interp_maybe_batched, tb)
            delayed_input_state = InputState(*interp_tb, delay_dist=new_delay_dist)
        else:
            raise ValueError(f"Interpolation method {self.interp} not supported.")
        return delayed_input_state

    def get_alpha(self, delay: Union[float, jax.typing.ArrayLike]) -> Union[float, jax.typing.ArrayLike]:
        """
        Get the alpha value of the delay distribution.

        Args:
            delay: the delay value

        Returns:
            The alpha value
        """
        return jnp.clip(self._get_alpha(delay, self.min, self.max), 0.0, 1.0)

    @staticmethod
    def _get_alpha(
        delay: Union[float, jax.typing.ArrayLike],
        min: Union[float, jax.typing.ArrayLike],
        max: Union[float, jax.typing.ArrayLike],
    ) -> Union[float, jax.typing.ArrayLike]:
        return (delay - min) / (max - min)


@struct.dataclass
class InputState:
    """A ring buffer that holds the inputs for a node's input channel.

    The size of the buffer is determined by the window size of the corresponding connection
    (i.e. node.connect(..., window=...)).

    Attributes:
        seq: the sequence number of the received message
        ts_sent: the time the message was sent
        ts_recv: the time the message was received
        data: the message of the connection (arbitrary pytree structure)
        delay_dist: the delay distribution of the connection
    """

    seq: ArrayLike
    ts_sent: ArrayLike
    ts_recv: ArrayLike
    data: Output  # --> must be a pytree where the shape of every leaf will become (size, *leafs.shape)
    delay_dist: DelayDistribution

    @classmethod
    def from_outputs(
        cls,
        seq: ArrayLike,
        ts_sent: ArrayLike,
        ts_recv: ArrayLike,
        outputs: Any,
        delay_dist: DelayDistribution,
        is_data: bool = False,
    ) -> "InputState":
        """Create an InputState from a list of messages, timestamps, and sequence numbers.

        The oldest message should be first in the list.

        Args:
            seq: the sequence number of the received message
            ts_sent: the time the message was sent
            ts_recv: the time the message was received
            outputs: the messages of the connection (arbitrary pytree structure)
            is_data: if True, the outputs are already a stacked pytree structure
            delay_dist: the delay distribution of the connection

        Returns:
            The input state with the messages and timestamps in the ring buffer.
        """

        data = jax.tree_util.tree_map(lambda *o: jnp.stack(o, axis=0), *outputs) if not is_data else outputs
        return cls(seq=seq, ts_sent=ts_sent, ts_recv=ts_recv, data=data, delay_dist=delay_dist)

    def _shift(self, a: ArrayLike, new: ArrayLike):
        rolled_a = jnp.roll(a, -1, axis=0)
        new_a = jnp.array(rolled_a).at[-1].set(jnp.array(new))
        return new_a

    def push(self, seq: int, ts_sent: float, ts_recv: float, data: Any) -> "InputState":
        """
        Push a new message into the ring buffer.

        Args:
            seq: the sequence number of the received message
            ts_sent: the time the message was sent
            ts_recv: the time the message was received
            data: the message of the connection (arbitrary pytree structure)

        Returns:
            The new input state with the message pushed into the ring buffer.
        """
        size = self.seq.shape[0]
        tb = [self.seq, self.ts_sent, self.ts_recv, self.data]
        new_t = [seq, ts_sent, ts_recv, data]

        # get new values
        if size > 1:
            new = jax.tree_util.tree_map(lambda tb, t: self._shift(tb, t), tb, new_t)
        else:
            new = jax.tree_util.tree_map(lambda _tb, _t: jnp.array(_tb).at[0].set(_t), tb, new_t)
        return InputState(*new, delay_dist=self.delay_dist)

    def __getitem__(self, val: int) -> "InputState":
        """Get the value of the ring buffer at a specific index.

        This is useful for indexing all the values of the ring buffer at a specific index.

        Args:
            val: the index to get the value from

        Returns:
            The input state at the specific index

        """
        tb = [self.seq, self.ts_sent, self.ts_recv, self.data]
        return InputState(*jax.tree_util.tree_map(lambda _tb: _tb[val], tb), delay_dist=self.delay_dist)


@struct.dataclass
class StepState:
    """
    Step state definition.

    It holds all the information that is required to step a node.

    Attributes:
        rng: The random number generator. Used for sampling random processes. If used, it should be updated.
        state: The state of the node. Usually dynamic during an episode.
        params: The parameters of the node. Usually static during an episode.
        inputs: The inputs of the node. See InputState.
        eps: The current episode number. Relates to the computation graph, not the episode counter of an environment.
        seq: The current step number. Automatically increases by 1 every step.
        ts: The current time step at the start of the step. Determined by the computation graph.
    """

    rng: jax.Array
    state: State
    params: Params
    inputs: FrozenDict[str, InputState] = struct.field(pytree_node=True, default_factory=lambda: None)
    eps: Union[int, ArrayLike] = struct.field(pytree_node=True, default_factory=lambda: onp.int32(0))
    seq: Union[int, ArrayLike] = struct.field(pytree_node=True, default_factory=lambda: onp.int32(0))
    ts: Union[float, ArrayLike] = struct.field(pytree_node=True, default_factory=lambda: onp.float32(0.0))


class _NoVal:
    pass


@struct.dataclass
class _StepStateDict:
    graph_state: "GraphState"

    def __getitem__(self, item) -> StepState:
        """
        Get the StepState for a node in the graph.

        Args:
            item: the node name

        Returns:
            The StepState for the node
        """
        rng = self.graph_state.rng.get(item, None) if self.graph_state.rng is not None else None
        eps = self.graph_state.eps
        seq = self.graph_state.seq.get(item, None) if self.graph_state.seq is not None else None
        ts = self.graph_state.ts.get(item, None) if self.graph_state.ts is not None else None
        params = self.graph_state.params.get(item, None) if self.graph_state.params is not None else None
        state = self.graph_state.state.get(item, None) if self.graph_state.state is not None else None
        inputs = self.graph_state.inputs.get(item, None) if self.graph_state.inputs is not None else None
        return StepState(rng=rng, seq=seq, eps=eps, ts=ts, params=params, state=state, inputs=inputs)

    def __len__(self):
        # get max len of all fields
        return max(
            len(self.graph_state.rng),
            # len(self.graph_state.eps),
            len(self.graph_state.seq),
            len(self.graph_state.ts),
            len(self.graph_state.params),
            len(self.graph_state.state),
            len(self.graph_state.inputs),
        )

    def __iter__(self):
        return iter(self.keys())

    def keys(self):
        # Return union of all keys
        return set(
            list(self.graph_state.rng.keys())
            # + list(self.graph_state.eps.keys())
            + list(self.graph_state.seq.keys())
            + list(self.graph_state.ts.keys())
            + list(self.graph_state.params.keys())
            + list(self.graph_state.state.keys())
            + list(self.graph_state.inputs.keys())
        )

    def items(self):
        return [(k, self[k]) for k in self.keys()]

    def values(self):
        return [self[k] for k in self.keys()]

    def get(self, key, default=_NoVal):
        if key in self.keys():
            return self[key]
        if default is _NoVal:
            raise KeyError(key)
        return default


@struct.dataclass
class GraphState:
    """Graph state definition.

    It holds all the information that is required to step a graph.

    Attributes:
        step: The current step number. Automatically increases by 1 every step.
        eps: The current episode number. To update the episode, use GraphState.replace_eps.
        rng: The random number generators for each node in the graph.
        seq: The current step number for each node in the graph.
        ts: The start time of the step for each node in the graph.
        params: The parameters for each node in the graph.
        state: The state for each node in the graph.
        inputs: The inputs for each node in the graph.
        timings_eps: The timings data structure that describes the execution and partitioning of the graph.
        buffer: The output buffer of the graph. It holds the outputs of nodes during the execution. Input buffers are
                automatically filled with the outputs of previously executed step calls of other nodes.
        aux: Auxiliary data that can be used to store additional information (e.g. records, wrappers etc.).
    """

    # The number of partitions (excl. supervisor) have run in the current episode.
    step: Union[int, ArrayLike] = struct.field(pytree_node=True, default_factory=lambda: onp.int32(0))
    eps: Union[int, ArrayLike] = struct.field(pytree_node=True, default_factory=lambda: onp.int32(0))
    # Step state components for each node in the graph.
    rng: FrozenDict[str, jax.Array] = struct.field(pytree_node=True, default_factory=lambda: FrozenDict({}))
    seq: FrozenDict[str, Union[int, ArrayLike]] = struct.field(pytree_node=True, default_factory=lambda: FrozenDict({}))
    ts: FrozenDict[str, Union[float, ArrayLike]] = struct.field(pytree_node=True, default_factory=lambda: FrozenDict({}))
    params: FrozenDict[str, Params] = struct.field(pytree_node=True, default_factory=lambda: FrozenDict({}))
    state: FrozenDict[str, State] = struct.field(pytree_node=True, default_factory=lambda: FrozenDict({}))
    inputs: FrozenDict[str, FrozenDict[str, InputState]] = struct.field(
        pytree_node=True, default_factory=lambda: FrozenDict({})
    )
    # The timings for a single episode (i.e. GraphState.timings[eps]).
    timings_eps: Timings = struct.field(pytree_node=True, default_factory=lambda: None)
    # A ring buffer that holds the outputs for every node's output channel.
    buffer: FrozenDict[str, Output] = struct.field(pytree_node=True, default_factory=lambda: None)
    # Some auxiliary data that can be used to store additional information (e.g. wrappers
    aux: FrozenDict[str, Any] = struct.field(pytree_node=True, default_factory=lambda: FrozenDict({}))

    @property
    def step_state(self) -> _StepStateDict:
        """A dictionary-like object that returns a StepState for each node in the graph."""
        return _StepStateDict(self)

    def replace_buffer(self, outputs: Union[Dict[str, Output], FrozenDict[str, Output]]) -> "GraphState":
        """Replace the buffer with new outputs.

        Generally not used by the user, but by the graph itself.
        """
        return self.replace(buffer=self.buffer.copy(outputs))

    def replace_eps(self, timings: Timings, eps: Union[int, ArrayLike]) -> "GraphState":
        """Replace the current episode number and corresponding timings corresponding to the episode.

        :param timings: The timings data structure that contains all timings for all episodes. Can be retrieved from the graph
                        with graph.timings.
        :param eps: The new episode number.
        :return: A new GraphState with the updated episode number and timings.
        """
        # Next(iter()) is a bit hacky, but it simply takes a node and counts the number of eps.
        max_eps = next(iter(timings.slots.values())).run.shape[-2]
        eps = jnp.clip(eps, onp.int32(0), max_eps - 1)
        timings_eps = rjax.tree_take(timings, eps)
        return self.replace(eps=eps, timings_eps=timings_eps)

    def replace_step(self, timings: Timings, step: Union[int, ArrayLike]) -> "GraphState":
        """Replace the current step number.

        :param timings: The timings data structure that contains all timings for all episodes. Can be retrieved from the graph
                        with graph.timings.
        :param step: The new step number.
        :return: A new GraphState with the updated step number.
        """
        # Next(iter()) is a bit hacky, but it simply takes a node and counts the number of steps.
        max_step = next(iter(timings.slots.values())).run.shape[-1]
        step = jnp.clip(step, onp.int32(0), max_step - 1)
        return self.replace(step=step)

    def replace_step_states(self, step_states: Union[Dict[str, StepState], FrozenDict[str, StepState]]) -> "GraphState":
        rng, seq, ts, params, state, inputs = {}, {}, {}, {}, {}, {}
        for n, ss in step_states.items():
            rng[n] = ss.rng
            seq[n] = ss.seq
            ts[n] = ss.ts
            params[n] = ss.params
            state[n] = ss.state
            inputs[n] = ss.inputs
        return self.replace(
            rng=self.rng.copy(rng),
            seq=self.seq.copy(seq),
            ts=self.ts.copy(ts),
            params=self.params.copy(params),
            state=self.state.copy(state),
            inputs=self.inputs.copy(inputs),
        )

    def replace_aux(self, aux: Union[Dict[str, Any], FrozenDict[str, Any]]) -> "GraphState":
        """Replace the auxillary data of the graph.

        :param aux: The new auxillary data.
        :return: A new GraphState with the updated auxillary data.
        """
        return self.replace(aux=self.aux.copy(aux))

    def try_get_aux(self, aux_name: str) -> Union[Any, None]:
        """Try to get auxillary data of the graph if it exists.

        :param aux_name: The name of the aux.
        :return: The aux of the node if it exists, else None.
        """
        return self.aux.get(aux_name, None)


# LOGGING


@struct.dataclass
class InputInfo:
    """
    A data structure that holds information about the input connection.

    Attributes:
        rate: The rate of the connection.
        window: The window size of the connection.
        blocking: Whether the connection is blocking.
        skip: Whether the connection is skipped.
        jitter: The jitter of the connection.
        phase: The phase of the connection.
        delay_dist: The delay distribution of the connection.
        delay: The delay of the connection.
        name: The name of the connection.
        output: The name of the output node.
    """

    rate: float
    window: int
    blocking: bool
    skip: bool
    jitter: constants.Jitter = struct.field(pytree_node=False)
    phase: float
    delay_dist: DelayDistribution
    delay: float
    name: str = struct.field(pytree_node=False)
    output: str = struct.field(pytree_node=False)


@struct.dataclass
class NodeInfo:
    """
    A data structure that holds information about the node.

    Attributes:
        rate: The rate of the node.
        advance: Whether the node advances the episode.
        scheduling: The scheduling of the node.
        phase: The phase of the node.
        delay_dist: The delay distribution of the node.
        delay: The delay of the node.
        inputs: The inputs of the node.
        name: The name of the node.
        cls: The class of the node.
        color: The color of the node.
        order: The order of the node.
    """

    rate: float
    advance: bool
    scheduling: constants.Scheduling = struct.field(pytree_node=False)
    phase: float
    delay_dist: DelayDistribution
    delay: float
    inputs: Dict[str, InputInfo]  # Uses name of output node in graph context, not the input_name
    name: str = struct.field(pytree_node=False)
    cls: str = struct.field(pytree_node=False)
    color: str = struct.field(pytree_node=False)
    order: int = struct.field(pytree_node=False)


@struct.dataclass
class Header:
    """
    A data structure that holds the header information of a record.

    Attributes:
        eps: The episode number.
        seq: The step number.
        ts: The time
    """

    eps: Union[int, jax.typing.ArrayLike]
    seq: Union[int, jax.typing.ArrayLike]
    ts: Union[float, jax.typing.ArrayLike]


@struct.dataclass
class MessageRecord:
    """
    A data structure that holds information about a sent or received message.

    Attributes:
        seq_out: The sequence number of the sent message.
        seq_in: The sequence number of the received message.
        ts_sent: The time the message was sent.
        ts_recv: The time the message was received.
        delay: The delay of the message.
    """

    seq_out: Union[int, jax.typing.ArrayLike]  # todo: If never sent, set to -1?
    seq_in: Union[int, jax.typing.ArrayLike]  # Corresponds to StepRecord.seq. If never received, set to -1.
    ts_sent: Union[float, jax.typing.ArrayLike]  # used to be sent: Header todo: what if never sent?
    ts_recv: Union[float, jax.typing.ArrayLike]  # used to be received: Header  todo: what if never sent?
    delay: Union[float, jax.typing.ArrayLike]


@struct.dataclass
class InputRecord:
    """
    A data structure that holds information about the input connection.

    Attributes:
        info: The input information.
        messages: The message record.
    """

    info: InputInfo = struct.field(pytree_node=False)  # This may have broken backward compatibility
    messages: MessageRecord


@struct.dataclass
class StepRecord:
    """
    A data structure that holds information about a step.

    Attributes:
        eps: The episode number.
        seq: The step number.
        ts_start: The start time of the step.
        ts_end: The end time of the step.
        delay: The delay of the step.
        rng: The random number generator.
        inputs: The input state.
        state: The state of the node.
        output: The output of the node
    """

    eps: Union[int, jax.typing.ArrayLike]
    seq: Union[int, jax.typing.ArrayLike]
    ts_start: Union[float, jax.typing.ArrayLike]
    ts_end: Union[float, jax.typing.ArrayLike]
    delay: Union[float, jax.typing.ArrayLike]
    rng: jax.Array  # Optionally logged
    inputs: InputState  # Optionally logged (can become very large)
    state: Base  # Optionally logged | Before the step call
    output: Base  # Optionally logged | After the step call


@struct.dataclass
class AsyncStepRecord(StepRecord):
    """
    A data structure that holds information about an asynchronous step.

    Attributes:
        ts_scheduled: The scheduled time of the step.
        ts_max: The maximum time of the step.
        ts_end_prev: The end time of the previous step.
        phase: The phase of the step.
        phase_scheduled: The scheduled phase of the step.
        phase_inputs: The phase of the inputs.
        phase_last: The last phase of the step.
        sent: The header of the sent message.
        phase_overwrite: The phase overwrite.
    """

    ts_scheduled: Union[float, jax.typing.ArrayLike]
    ts_max: Union[float, jax.typing.ArrayLike]
    ts_end_prev: Union[float, jax.typing.ArrayLike]
    phase: Union[float, jax.typing.ArrayLike]
    phase_scheduled: Union[float, jax.typing.ArrayLike]
    phase_inputs: Union[float, jax.typing.ArrayLike]
    phase_last: Union[float, jax.typing.ArrayLike]
    sent: Header
    phase_overwrite: Union[float, jax.typing.ArrayLike]


@struct.dataclass
class NodeRecord:
    """
    A data structure that holds information about a node.

    Attributes:
        info: The node information.
        clock: The clock of the node.
        real_time_factor: The real time factor of the node.
        ts_start: The start time of the node.
        params: The parameters of the node.
        inputs: The input record.
        steps: The step record.
    """

    info: NodeInfo = struct.field(pytree_node=False)
    clock: constants.Clock = struct.field(pytree_node=False)
    real_time_factor: float = struct.field(pytree_node=False)
    ts_start: float
    params: Base
    inputs: Dict[str, InputRecord]  # Uses name of output node in graph context, not the input_name
    steps: StepRecord


@struct.dataclass
class EpisodeRecord:
    """
    A data structure that holds recorded data of an episode.

    Attributes:
        nodes: The node records.
    """

    nodes: Dict[str, NodeRecord]

    def __getitem__(self, val: int) -> "EpisodeRecord":
        """
        Get the value of the episode record at a specific index.

        Args:
            val: the index to get the value from

        Returns:
            The episode record at the specific index
        """
        return jax.tree_util.tree_map(lambda x: x[val], self)

    def filter(self, nodes: Dict[str, "BaseNode"], filter_connections: bool = False) -> "EpisodeRecord":
        """
        Filter the episode record.

        Args:
            nodes: Only keep record.nodes in of subgraph spanned by nodes.
            filter_connections: If True, only keep connections between nodes in nodes.

        Returns:
            A new episode record with only the nodes and connections in nodes.
        """
        # Determine set of nodes and connections to keep
        connections = set()
        for n2, v2 in nodes.items():
            if v2.inputs is None:
                raise NotImplementedError(
                    "'inputs' not available. Records logged in Clock.COMPILED mode do not log inputs, "
                    "so the graph cannot be reconstructed."
                )
            if filter_connections:  # Also filter connections that only exist between nodes in `nodes`
                for n1, i in v2.inputs.items():
                    if n1 in nodes:
                        connections.add((n1, n2))
            else:  # Only filters nodes, meaning self.nodes may have more connections than nodes.
                if n2 in self.nodes:
                    for n1, v1 in self.nodes[n2].inputs.items():
                        if n1 in nodes:
                            connections.add((n1, n2))

        # Filter nodes and connections (if filter_connections=True)
        new_nodes = {n: self.nodes[n] for n in nodes}
        for n2, v2 in new_nodes.items():
            new_info_inputs = {n1: v2.info.inputs[n1] for n1 in v2.inputs if (n1, n2) in connections}
            new_info = v2.info.replace(inputs=new_info_inputs)
            new_inputs = {n1: v2.inputs[n1] for n1 in v2.inputs if (n1, n2) in connections}
            new_nodes[n2] = v2.replace(info=new_info, inputs=new_inputs)
        return EpisodeRecord(nodes=new_nodes)

    def to_graph(self) -> Graph:
        """
        Convert the episode record to a graph.

        Returns:
            The graph of the episode record.
        """
        vertices = {
            n: Vertex(seq=v.steps.seq, ts_start=v.steps.ts_start, ts_end=v.steps.ts_end) for n, v in self.nodes.items()
        }
        edges = dict()
        for n2, v2 in self.nodes.items():
            if v2.inputs is None:
                raise NotImplementedError(
                    "'inputs' not available. Records logged in Clock.COMPILED mode do not log inputs, "
                    "so the graph cannot be reconstructed."
                )
            for n1, i in v2.inputs.items():
                seq_in = i.messages.seq_in
                seq_out = i.messages.seq_out
                ts_recv = i.messages.ts_recv
                edges[(n1, n2)] = Edge(seq_out=seq_out, seq_in=seq_in, ts_recv=ts_recv)
        return Graph(vertices=vertices, edges=edges)


@struct.dataclass
class ExperimentRecord:
    """
    A data structure that holds recorded data of an experiment.

    Attributes:
        episodes: The episode records.
    """

    episodes: List[EpisodeRecord]

    def filter(self, nodes: Dict[str, "BaseNode"], filter_connections: bool = False) -> "ExperimentRecord":
        episodes = [e.filter(nodes, filter_connections=filter_connections) for e in self.episodes]
        return ExperimentRecord(episodes=episodes)

    def to_graph(self) -> Graph:
        # Note: Vertex.seq=-1, .ts_start=-1., .ts_end=-1. for padded vertices
        # Note: Edge.seq_out=-1, .seq_in=-1., .ts_recv=-1. for padded edges or edges that were never received.
        # Convert to graphs
        graphs_raw = [e.to_graph() for e in self.episodes]
        return Graph.stack(graphs_raw)

    def stack(self, method: str = "padded") -> EpisodeRecord:
        if method == "padded":
            return self._padded_stack(fill_value=-1)  # Currently fixed to -1, as this is expected in "episode.to_graph"
        elif method == "truncated":
            return self._truncated_stack()
        else:
            raise NotImplementedError(f"Method {method} not implemented.")

    def _padded_stack(self, fill_value) -> EpisodeRecord:
        def _pad(*x):
            try:
                res = onp.array(x)
            except ValueError:
                _max_len = max(len(arr) for arr in x)
                zero_pad_widths = [(0, 0)] * (x[0].ndim - 1)
                # Pad with -1
                _padded = list(
                    onp.pad(arr, [(0, _max_len - len(arr))] + zero_pad_widths, constant_values=fill_value) for arr in x
                )
                res = onp.array(_padded)
            return res

        stacked = jax.tree_util.tree_map(_pad, *self.episodes)
        return stacked

    def _truncated_stack(self) -> EpisodeRecord:
        raise NotImplementedError("Truncated stacking is not yet implemented.")


# System identification
Filter = Dict[str, Params]


@struct.dataclass
class Transform:
    """A transformation that can be applied to parameters.

    Can be used to normalize, denormalize, or transform parameters in any way.
    """

    @classmethod
    def init(cls, *args: Any, **kwargs: Any) -> "Transform":
        """Initialize the transform.

        Args:
            *args: The arguments to initialize the transform.
            **kwargs: The keyword arguments to initialize the transform.

        Returns:
            The initialized transform.
        """
        raise NotImplementedError

    def apply(self, params: Dict[str, Params]) -> Dict[str, Params]:
        """Apply the transformation to the parameters.

        Args:
            params: The original parameters.

        Returns:
            The transformed parameters.
        """
        raise NotImplementedError

    def inv(self, params: Dict[str, Params]) -> Dict[str, Params]:
        """Invert the transformation.

        Args:
            params: The transformed parameters.

        Returns:
            The original parameters.
        """
        raise NotImplementedError


Loss = Callable[[Params, Transform, jax.Array], Union[float, jax.Array]]


@struct.dataclass
class Identity(Transform):
    """The identity transformation (NOOP)."""

    @classmethod
    def init(cls) -> "Identity":
        """
        Initialize the identity transformation.

        Returns:
            The identity transformation.
        """
        return cls()

    def apply(self, params: Params) -> Params:
        """
        Apply the identity transformation (NOOP).

        Args:
            params: The parameters.

        Returns:
            The same parameters.
        """
        return params

    def inv(self, params: Params) -> Params:
        """
        Invert the identity transformation (NOOP).

        Args:
            params: The parameters.

        Returns:
            The same parameters.
        """
        return params


@struct.dataclass
class Chain(Transform):
    """
    Chain multiple transformations together.

    Attributes:
        transforms: The transformations to chain together.
    """

    transforms: Sequence[Transform]

    @classmethod
    def init(cls, *transforms: Sequence[Transform]) -> "Chain":
        """Initialize the chain of transformations.

        Args:
            *transforms: The transformations to chain together. The order of the transformations is important.

        Returns:
            The chain of transformations.
        """
        return cls(transforms=transforms)

    def apply(self, params: Params) -> Params:
        """Apply the chain of transformations to the parameters.

        Args:
            params: The parameters.

        Returns:
            The transformed parameters.
        """
        _intermediate = params
        for t in self.transforms:
            _intermediate = t.apply(_intermediate)
        return _intermediate

    def inv(self, params: Params) -> Params:
        """
        Invert the chain of transformations.

        Args:
            params: The transformed parameters.

        Returns:
            The original parameters.
        """
        _intermediate = params
        for t in self.transforms[::-1]:
            _intermediate = t.inv(_intermediate)
        return _intermediate


@struct.dataclass
class Extend(Transform):
    """
    Extend the structure of a pytree with additional parameters from another pytree.

    Useful when you only want to optimize a subset of the parameters, but the full structure is required for simulation.

    Example:
        ```python
        from rex.base import Extend
        base_params = {"a": {"b": 0, "c": "1"}, "d": 2}
        opt_params = {"a": None, "d": 99}

        transform = Extend.init(base_params, opt_params)
        extended = transform.apply(opt_params) # {"a": {"b": 0, "c": "1"}, "b": 99}
        filtered = transform.inv(extended) # {"a": None, "d": 99}
        ```

    Attributes:
        base_params: The base parameters.
        mask: The mask of the extended parameters.
    """

    base_params: Params
    mask: Params

    @classmethod
    def init(cls, base_params: Params, opt_params: Params = None) -> "Extend":
        """Initialize the extend transformation.

        Args:
            base_params: The base parameters.
            opt_params: The structure of the params that is going to be extended with the base parameters.

        Returns:
            The extend transformation.
        """
        mask = jax.tree_util.tree_map(lambda ex_x: ex_x is not None, opt_params)
        ret = cls(base_params=base_params, mask=mask)
        _ = ret.apply(opt_params)  # Test structure
        return ret

    def extend(self, params: Params) -> Params:
        params_extended_pytree = rjax.tree_extend(self.base_params, params)
        params_extended = jax.tree_util.tree_map(
            lambda base_x, ex_x: base_x if ex_x is None else ex_x, self.base_params, params_extended_pytree
        )
        return params_extended

    def filter(self, params_extended: Params) -> Params:
        mask_ex = rjax.tree_extend(self.base_params, self.mask)
        filtered_ex = eqx.filter(params_extended, mask_ex)
        filtered_ex_flat, _ = jax.tree_util.tree_flatten(filtered_ex)
        _, mask_filt_treedef = jax.tree_util.tree_flatten(self.mask)
        filtered = jax.tree_util.tree_unflatten(mask_filt_treedef, filtered_ex_flat)
        return filtered

    def apply(self, params: Params) -> Params:
        """
        Apply the extend transformation to the parameters.

        Args:
            params: The parameters.

        Returns:
            The extended parameters to the structure of the base parameters.
        """
        return self.extend(params)

    def inv(self, params: Params) -> Params:
        """
        Invert the extend transformation.

        Args:
            params: The extended parameters (i.e. structure of the base parameters).

        Returns:
            The original parameters (return to the structure of the opt_params).
        """
        return self.filter(params)


@struct.dataclass
class Denormalize(Transform):
    """
    (De)normalize the parameters to/from a [-1, 1] range.

    Attributes:
        scale: The scale of the original parameters.
        offset: The offset of the original parameters.
    """

    scale: Params
    offset: Params

    @classmethod
    def init(cls, min_params: Params, max_params: Params) -> "Denormalize":
        """
        Initialize the denormalize transformation

        Note: Non-zero scale is required.
            Therefore, the min and max values should be different for each parameter.

        Args:
            min_params: The minimum values of the original parameters.
            max_params: The maximum values of the original parameters.

        Returns:
            The denormalize transformation
        """
        offset = jax.tree_util.tree_map(lambda _min, _max: (_min + _max) / 2.0, min_params, max_params)
        scale = jax.tree_util.tree_map(lambda _min, _max: (_max - _min) / 2, min_params, max_params)
        zero_filter = jax.tree_util.tree_map(lambda _scale: _scale == 0.0, scale)
        try:
            if onp.array(jax.tree_util.tree_reduce(jnp.logical_or, zero_filter)).all():
                raise ValueError(
                    "The scale cannot be zero. Hint: Check if there are leafs with 'True' in the following zero_filter: "
                    f"{zero_filter}"
                )
        except jax.errors.TracerArrayConversionError:
            pass
        return cls(scale=scale, offset=offset)

    def normalize(self, params: Params) -> Params:
        params_norm = jax.tree_util.tree_map(
            lambda _params, _offset, _scale: (_params - _offset) / _scale, params, self.offset, self.scale
        )
        return params_norm

    def denormalize(self, params: Params) -> Params:
        params_unnorm = jax.tree_util.tree_map(
            lambda _params, _offset, _scale: _params * _scale + _offset, params, self.offset, self.scale
        )
        return params_unnorm

    def apply(self, params: Params) -> Params:
        """
        Apply the denormalize transformation to the parameters.

        Args:
            params: The normalized parameters.

        Returns:
            The denormalized parameters.
        """
        return self.denormalize(params)

    def inv(self, params: Params) -> Params:
        """
        Invert the denormalize transformation.

        Args:
            params: The denormalized parameters.

        Returns:
            The normalized parameters.
        """
        return self.normalize(params)


@struct.dataclass
class Exponential(Transform):
    """Apply the exponential transformation to the parameters."""

    @classmethod
    def init(cls) -> "Exponential":
        """Create an exponential transformation.

        Returns:
            The exponential transformation.
        """
        return cls()

    def apply(self, params: Params) -> Params:
        """
        Apply the exponential transformation to the parameters.

        Args:
            params: The parameters.

        Returns:
            The transformed parameters.
        """
        return jax.tree_util.tree_map(lambda x: jnp.exp(x), params)

    def inv(self, params: Params) -> Params:
        """
        Invert the exponential transformation.

        Args:
            params: The transformed parameters.

        Returns:
            The original parameters.
        """
        return jax.tree_util.tree_map(lambda x: jnp.log(x), params)


@struct.dataclass
class Shared(Transform):
    """
    A shared transformation that can be applied to parameters.

    Useful to share parameters between different parts of the model.

    Example:
        ```python
        where_fn = lambda p: p["a"]
        replace_fn = lambda p: p["b"]
        inverse_fn = lambda p: None
        transform = Shared.init(where=where_fn, replace_fn=replace_fn, inverse_fn=inverse_fn)

        opt_params = {"a": 1, "b": 2}
        applied = transform.apply(opt_params) # {"a": 2, "b": 2}
        inverted = transform.inv(applied)  # {"a": None, "b": 2}
        ```

    Attributes:
        where: The function that determines where to apply the transformation.
        replace_fn: The function that replaces the parameters.
        inverse_fn: The function that inverts the transformation.
    """

    where: Callable[[Any], Union[Any, Sequence[Any]]] = struct.field(pytree_node=False)
    replace_fn: Callable[[Any], Union[Any, Sequence[Any]]] = struct.field(pytree_node=False)
    inverse_fn: Callable[[Any], Union[Any, Sequence[Any]]] = struct.field(pytree_node=False)

    @classmethod
    def init(
        cls,
        where: Callable[[Any], Union[Any, Sequence[Any]]],
        replace_fn: Callable[[Any], Union[Any, Sequence[Any]]],
        inverse_fn: Callable[[Any], Union[Any, Sequence[Any]]] = lambda _tree: None,
    ) -> "Shared":
        """
        Initialize the shared transformation.

        Args:
            where: The function that determines where to apply the transformation.
            replace_fn: The function that replaces the parameters.
            inverse_fn: The function that inverts the transformation.

        Returns:
            The shared transformation.
        """
        return cls(where=where, replace_fn=replace_fn, inverse_fn=inverse_fn)

    def apply(self, params: Params) -> Params:
        """
        Apply the shared transformation to the parameters.

        Args:
            params: The parameters.

        Returns:
            The transformed parameters.
        """
        new = self.replace_fn(params)
        return eqx.tree_at(self.where, params, new, is_leaf=lambda x: x is None)

    def inv(self, params: Params) -> Params:
        """
        Invert the shared transformation

        Args:
            params: The transformed parameters.

        Returns:
            The original parameters.
        """
        new = self.inverse_fn(params)
        return eqx.tree_at(self.where, params, new, is_leaf=lambda x: x is None)
