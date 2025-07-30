# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0
from typing import Union
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from GridCalEngine.enumerations import DeviceType, BuildStatus
from GridCalEngine.Devices.Parents.load_parent import LoadParent
from GridCalEngine.Devices.profile import Profile


class Load(LoadParent):
    """
    Load
    """
    __slots__ = (
        'G',
        'B',
        'Ir',
        'Ii',
        '_G_prof',
        '_B_prof',
        '_Ir_prof',
        '_Ii_prof',
        '_n_customers',
        '_n_customers_prof',
    )

    def __init__(self, name='Load', idtag=None, code='',
                 G=0.0, B=0.0, Ir=0.0, Ii=0.0, P=0.0, Q=0.0, Cost=1200.0,
                 active=True, mttf=0.0, mttr=0.0, capex=0, opex=0,
                 build_status: BuildStatus = BuildStatus.Commissioned):
        """
        The load object implements the so-called ZIP model, in which the load can be
        represented by a combination of power (P), current(I), and impedance (Z).
        The sign convention is: Positive to act as a load, negative to act as a generator.
        :param name: Name of the load
        :param idtag: UUID code
        :param code: secondary ID code
        :param G: Conductance in equivalent MW
        :param B: Susceptance in equivalent MVAr
        :param Ir: Real current in equivalent MW
        :param Ii: Imaginary current in equivalent MVAr
        :param P: Active power in MW
        :param Q: Reactive power in MVAr
        :param Cost: Cost of load shedding
        :param active: Is the load active?
        :param mttf: Mean time to failure in hours
        :param mttr: Mean time to recovery in hours
        """
        LoadParent.__init__(self,
                            name=name,
                            idtag=idtag,
                            code=code,
                            bus=None,
                            cn=None,
                            active=active,
                            P=P,
                            Q=Q,
                            Cost=Cost,
                            mttf=mttf,
                            mttr=mttr,
                            capex=capex,
                            opex=opex,
                            build_status=build_status,
                            device_type=DeviceType.LoadDevice)

        self.G = float(G)
        self.B = float(B)
        self.Ir = float(Ir)
        self.Ii = float(Ii)

        self._G_prof = Profile(default_value=self.G, data_type=float)
        self._B_prof = Profile(default_value=self.B, data_type=float)
        self._Ir_prof = Profile(default_value=self.Ir, data_type=float)
        self._Ii_prof = Profile(default_value=self.Ii, data_type=float)

        self._n_customers: int = 1
        self._n_customers_prof = Profile(default_value=self._n_customers, data_type=int)

        self.register(key='Ir', units='MW', tpe=float,
                      definition='Active power of the current component at V=1.0 p.u.', profile_name='Ir_prof')
        self.register(key='Ii', units='MVAr', tpe=float,
                      definition='Reactive power of the current component at V=1.0 p.u.', profile_name='Ii_prof')
        self.register(key='G', units='MW', tpe=float,
                      definition='Active power of the impedance component at V=1.0 p.u.', profile_name='G_prof')
        self.register(key='B', units='MVAr', tpe=float,
                      definition='Reactive power of the impedance component at V=1.0 p.u.', profile_name='B_prof')
        self.register(key='n_customers', units='unit', tpe=int,
                      definition='Number of customers represented by this load', profile_name='n_customers_prof')

    @property
    def Ir_prof(self) -> Profile:
        """
        Cost profile
        :return: Profile
        """
        return self._Ir_prof

    @Ir_prof.setter
    def Ir_prof(self, val: Union[Profile, np.ndarray]):
        if isinstance(val, Profile):
            self._Ir_prof = val
        elif isinstance(val, np.ndarray):
            self._Ir_prof.set(arr=val)
        else:
            raise Exception(str(type(val)) + 'not supported to be set into a Ir_prof')

    @property
    def Ii_prof(self) -> Profile:
        """
        Cost profile
        :return: Profile
        """
        return self._Ii_prof

    @Ii_prof.setter
    def Ii_prof(self, val: Union[Profile, np.ndarray]):
        if isinstance(val, Profile):
            self._Ii_prof = val
        elif isinstance(val, np.ndarray):
            self._Ii_prof.set(arr=val)
        else:
            raise Exception(str(type(val)) + 'not supported to be set into a Ii_prof')

    @property
    def G_prof(self) -> Profile:
        """
        Cost profile
        :return: Profile
        """
        return self._G_prof

    @G_prof.setter
    def G_prof(self, val: Union[Profile, np.ndarray]):
        if isinstance(val, Profile):
            self._G_prof = val
        elif isinstance(val, np.ndarray):
            self._G_prof.set(arr=val)
        else:
            raise Exception(str(type(val)) + 'not supported to be set into a G_prof')

    @property
    def B_prof(self) -> Profile:
        """
        Cost profile
        :return: Profile
        """
        return self._B_prof

    @B_prof.setter
    def B_prof(self, val: Union[Profile, np.ndarray]):
        if isinstance(val, Profile):
            self._B_prof = val
        elif isinstance(val, np.ndarray):
            self._B_prof.set(arr=val)
        else:
            raise Exception(str(type(val)) + 'not supported to be set into a B_prof')

    @property
    def n_customers(self) -> int:
        """
        Return the number of customers
        """
        return self._n_customers

    @n_customers.setter
    def n_customers(self, val: int):
        """
        Set the number of customers
        :param val: value greater than 0
        """
        try:
            val2 = int(val)
            if val2 > 0:
                self._n_customers = val2
            else:
                print("There must be at least one customer right?")
        except ValueError as e:
            print(e)

    @property
    def n_customers_prof(self) -> Profile:
        """
        Cost profile
        :return: Profile
        """
        return self._n_customers_prof

    @n_customers_prof.setter
    def n_customers_prof(self, val: Union[Profile, np.ndarray]):
        if isinstance(val, Profile):
            self._n_customers_prof = val
        elif isinstance(val, np.ndarray):
            self._n_customers_prof.set(arr=val)
        else:
            raise Exception(str(type(val)) + 'not supported to be set into n_customers_prof')

    def plot_profiles(self, time=None, show_fig=True):
        """
        Plot the time series results of this object
        :param time: array of time values
        :param show_fig: Show the figure?
        """

        if time is not None:
            fig = plt.figure(figsize=(12, 8))

            ax_1 = fig.add_subplot(211)
            ax_2 = fig.add_subplot(212, sharex=ax_1)

            # P
            y = self.P_prof.toarray()
            df = pd.DataFrame(data=y, index=time, columns=[self.name])
            ax_1.set_title('Active power', fontsize=14)
            ax_1.set_ylabel('MW', fontsize=11)
            df.plot(ax=ax_1)

            # Q
            y = self.Q_prof.toarray()
            df = pd.DataFrame(data=y, index=time, columns=[self.name])
            ax_2.set_title('Reactive power', fontsize=14)
            ax_2.set_ylabel('MVAr', fontsize=11)
            df.plot(ax=ax_2)

            plt.legend()
            fig.suptitle(self.name, fontsize=20)

            if show_fig:
                plt.show()
