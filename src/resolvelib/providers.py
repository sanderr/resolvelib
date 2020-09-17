class AbstractProvider(object):
    """Delegate class to provide requirement interface for the resolver."""

    def identify(self, requirement_or_candidate):
        """Given a requirement or candidate, return an identifier for it.

        This is used in many places to identify a requirement or candidate,
        e.g. whether two requirements should have their specifier parts merged,
        whether two candidates would conflict with each other (because they
        have same name but different versions).
        """
        raise NotImplementedError

    def get_preference(self, resolution, candidates, information):
        """Produce a sort key for given requirement based on preference.

        The preference is defined as "I think this requirement should be
        resolved first". The lower the return value is, the more preferred
        this group of arguments is.

        :param resolution: Currently pinned candidate, or `None`.
        :param candidates: A list of possible candidates.
        :param information: A list of requirement information.

        Each information instance is a named tuple with two entries:

        * `requirement` specifies a requirement contributing to the current
          candidate list
        * `parent` specifies the candidate that provides (dependend on) the
          requirement, or `None` to indicate a root requirement.

        The preference could depend on a various of issues, including (not
        necessarily in this order):

        * Is this package pinned in the current resolution result?
        * How relaxed is the requirement? Stricter ones should probably be
          worked on first? (I don't know, actually.)
        * How many possibilities are there to satisfy this requirement? Those
          with few left should likely be worked on first, I guess?
        * Are there any known conflicts for this requirement? We should
          probably work on those with the most known conflicts.

        A sortable value should be returned (this will be used as the `key`
        parameter of the built-in sorting function). The smaller the value is,
        the more preferred this requirement is (i.e. the sorting function
        is called with `reverse=False`).
        """
        raise NotImplementedError

    def find_matches(self, identifier, requirements):
        """Find all possible candidates satisfying all identified requirements.

        This should try to get candidates based on the requirements' types.
        For VCS, local, and archive requirements, the one-and-only match is
        returned, and for a "named" requirement, the index(es) should be
        consulted to find concrete candidates for this requirement.

        :param identifier: An identifier as returned by ``identify()``, that
            candidates returned by this function should identify as.
        :param requirements: A mapping of requirements the resolver knows.
            Each key is a requirement identifiers. Each value is a non-empty
            collection of requirements of that identifier. ``identifier`` is
            guarenteed to exist in the mapping.
        :returns: An iterable that orders candidates by preference, e.g. the
            most preferred candidate should come first.
        """
        raise NotImplementedError

    def is_satisfied_by(self, requirement, candidate):
        """Whether the given requirement can be satisfied by a candidate.

        The candidate is guarenteed to have been generated from the
        requirement.

        A boolean should be returned to indicate whether `candidate` is a
        viable solution to the requirement.
        """
        raise NotImplementedError

    def get_dependencies(self, candidate):
        """Get dependencies of a candidate.

        This should return a collection of requirements that `candidate`
        specifies as its dependencies.
        """
        raise NotImplementedError


class AbstractResolver(object):
    """The thing that performs the actual resolution work."""

    base_exception = Exception

    def __init__(self, provider, reporter):
        self.provider = provider
        self.reporter = reporter

    def resolve(self, requirements, **kwargs):
        """Take a collection of constraints, spit out the resolution result.

        This returns a representation of the final resolution state, with one
        guarenteed attribute ``mapping`` that contains resolved candidates as
        values. The keys are their respective identifiers.

        :param requirements: A collection of constraints.
        :param kwargs: Additional keyword arguments that subclasses may accept.

        :raises: ``self.base_exception`` or its subclass.
        """
        raise NotImplementedError
